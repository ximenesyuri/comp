import ast
import textwrap
from inspect import signature, Signature, Parameter, _empty, getsource, getsourcefile
from functools import update_wrapper
import re
import sys
from typed import typed, Function, Dict, Any, Str, Bool, Set, Tuple, TYPE
from app.mods.types.base import Jinja
from app.mods.helper.types import COMPONENT
from app.mods.helper.helper import _VAR_DELIM_START, _VAR_DELIM_END, _extract_raw_jinja

def _get_context(func):
    sig = signature(getattr(func, "func", func))
    if "__context__" in sig.parameters:
        param = sig.parameters["__context__"]
        if param.default != Parameter.empty and isinstance(param.default, dict):
            return param.default.copy()
    return {}

def _merge_context(*comps):
    merged = {}
    for comp in comps:
        merged.update(_get_context(comp))
    return merged

def _extract_recursive_globals(func):
    src = getsource(func)
    src = textwrap.dedent(src)
    tree = ast.parse(src)
    referenced = set()
    sig = signature(func)
    for param in sig.parameters.values():
        ann = param.annotation
        if isinstance(ann, str):
            referenced.add(ann.split('.')[-1])
        elif hasattr(ann, '__name__'):
            referenced.add(ann.__name__)
        default = param.default
        if hasattr(default, '__name__'):
            referenced.add(default.__name__)
    if sig.return_annotation is not _empty:
        ra = sig.return_annotation
        if isinstance(ra, str):
            referenced.add(ra.split('.')[-1])
        elif hasattr(ra, '__name__'):
            referenced.add(ra.__name__)
    class GlobalReferred(ast.NodeVisitor):
        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load):
                referenced.add(node.id)
        def visit_Attribute(self, node):
            self.generic_visit(node)
        def visit_FunctionDef(self, node):
            pass
        def visit_ClassDef(self, node):
            pass
    GlobalReferred().visit(tree)
    for param in sig.parameters.keys():
        referenced.discard(param)
    referenced -= set(__import__('builtins').__dict__.keys())
    return referenced

def _get_globals(func, extra_search_modules):
    base = func.__globals__.copy()
    needed = _extract_recursive_globals(func)
    missing = [name for name in needed if name not in base]
    for name in missing:
        found = False
        if name in globals():
            base[name] = globals()[name]
            continue
        if extra_search_modules:
            for mod in sys.modules.values():
                if mod and hasattr(mod, name):
                    base[name] = getattr(mod, name)
                    found = True
                    break
        if not found:
            pass
    return base

def _copy(func, **rename_map):
    if not callable(func):
        raise TypeError("copy_function expects a callable as input")

    seen = set()
    while hasattr(func, '__wrapped__') and func not in seen:
        seen.add(func)
        func = func.__wrapped__

    if not rename_map:
        def make_empty_deepcopy(f):
            co = f.__code__
            newf = type(f)(
                co.co_code, co.co_consts, co.co_names, co.co_varnames, co.co_argcount,
                co.co_flags, co.co_firstlineno, co.co_lnotab, co.co_freevars, co.co_cellvars,
                co.co_filename, co.co_name,
                f.__defaults__, f.__closure__
            )
            try:
                newf.__dict__.update(f.__dict__)
            except AttributeError:
                pass
            update_wrapper(newf, f)
            return newf
        return make_empty_deepcopy(func)

    src = getsource(func)
    src = textwrap.dedent(src)
    tree = ast.parse(src)

    class ParamRenamer(ast.NodeTransformer):
        def __init__(self, rename_map):
            self.rename_map = rename_map

        def visit_FunctionDef(self, node):
            for arg_obj in node.args.args:
                if arg_obj.arg in self.rename_map:
                    arg_obj.arg = self.rename_map[arg_obj.arg]
            for arg_obj in node.args.kwonlyargs:
                if arg_obj.arg in self.rename_map:
                    arg_obj.arg = self.rename_map[arg_obj.arg]
            if node.args.vararg and node.args.vararg.arg in self.rename_map:
                node.args.vararg.arg = self.rename_map[node.args.vararg.arg]
            if node.args.kwarg and node.args.kwarg.arg in self.rename_map:
                node.args.kwarg.arg = self.rename_map[node.args.kwarg.arg]

            self.generic_visit(node)
            return node

        def visit_Name(self, node):
            if node.id in self.rename_map:
                if isinstance(node.ctx, (ast.Load, ast.Store, ast.Del)):
                    node.id = self.rename_map[node.id]
            self.generic_visit(node)
            return node

        def visit_Attribute(self, node):
            if isinstance(node.value, ast.Name) and node.value.id in self.rename_map:
                node.value.id = self.rename_map[node.value.id]
            self.generic_visit(node)
            return node

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id in self.rename_map:
                node.func.id = self.rename_map[node.func.id]
            self.generic_visit(node)
            return node

        def visit_keyword(self, node):
            if node.arg and node.arg in self.rename_map:
                node.arg = self.rename_map[node.arg]
            self.generic_visit(node)
            return node

        def visit_JoinedStr(self, node):
            self.generic_visit(node)
            return node

        def visit_FormattedValue(self, node):
            self.visit(node.value)
            self.generic_visit(node)
            return node

    class StringDotRenamer(ast.NodeTransformer):
        def __init__(self, rename_map):
            self.rename_map = rename_map
        def visit_Constant(self, node):
            if isinstance(node.value, str):
                for k, v in self.rename_map.items():
                    node.value = re.sub(r'\b' + re.escape(k) + r'\.', re.escape(v) + '.', node.value)
            return node
        def visit_Str(self, node):
            if hasattr(node, 's'):
                for k, v in self.rename_map.items():
                    node.s = re.sub(r'\b' + re.escape(k) + r'\.', re.escape(v) + '.', node.s)
            return node

    class JinjaVarRenamer(ast.NodeTransformer):
        def __init__(self, rename_map, var_delim_start, var_delim_end):
            self.rename_map = rename_map
            self.var_delim_start = var_delim_start
            self.var_delim_end = var_delim_end
            self.pattern_cache = {}
        def _get_pattern(self, old_name):
            if old_name not in self.pattern_cache:
                self.pattern_cache[old_name] = re.compile(
                    re.escape(self.var_delim_start) + r'\s*\b' + re.escape(old_name) + r'\b\s*' + re.escape(self.var_delim_end)
                )
            return self.pattern_cache[old_name]
        def visit_Constant(self, node):
            if isinstance(node.value, str):
                new_value = node.value
                for old_name, new_name in self.rename_map.items():
                    pattern = self._get_pattern(old_name)
                    replacement_str = f"{self.var_delim_start} {new_name} {self.var_delim_end}"
                    new_value = pattern.sub(replacement_str, new_value)
                node.value = new_value
            return node
        def visit_Str(self, node):
            if hasattr(node, 's'):
                new_s = node.s
                for old_name, new_name in self.rename_map.items():
                    pattern = self._get_pattern(old_name)
                    replacement_str = f"{self.var_delim_start} {new_name} {self.var_delim_end}"
                    new_s = pattern.sub(replacement_str, new_s)
                node.s = new_s
            return node

    tree = ParamRenamer(rename_map).visit(tree)
    tree = StringDotRenamer(rename_map).visit(tree)
    tree = JinjaVarRenamer(rename_map, _VAR_DELIM_START, _VAR_DELIM_END).visit(tree)
    ast.fix_missing_locations(tree)

    copied_jinja_string = ""
    found_return_node = False

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            for item in ast.walk(node):
                if isinstance(item, ast.Return):
                    found_return_node = True
                    if isinstance(item.value, ast.JoinedStr):
                        if sys.version_info >= (3, 9):
                            unparsed_fstring = ast.unparse(item.value)
                            content_match = re.match(r'f?([\'"]{1,3})(.*)\1$', unparsed_fstring, re.DOTALL)
                            if content_match:
                                inner_f_string_content = content_match.group(2)
                                copied_jinja_string = _extract_raw_jinja(inner_f_string_content)
                    elif isinstance(item.value, ast.Constant):
                        if isinstance(item.value.value, str):
                            match = re.search(r'jinja\s*\n([\s\S]*?)', item.value.value)
                            if match:
                                copied_jinja_string = match.group(1)
                    break
            break

    globs = _get_globals(func, extra_search_modules=True)
    locs = {}

    exec(compile(tree, filename="<_copy_func>", mode="exec"), globs, locs)

    func_name = func.__name__
    if func_name not in locs:
        raise RuntimeError(f"Could not find function '{func_name}' in compiled code locals after AST transformation.")

    new_func = locs[func_name]
    update_wrapper(new_func, func)

    new_func._jinja = copied_jinja_string

    old_sig = signature(func)
    new_params = []
    new_annotations = {}
    for param in old_sig.parameters.values():
        if param.name in rename_map:
            new_name = rename_map[param.name]
            new_param = Parameter(
                new_name, kind=param.kind, default=param.default,
                annotation=param.annotation
            )
            new_params.append(new_param)
            if param.annotation is not _empty:
                new_annotations[new_name] = param.annotation
        else:
            new_params.append(param)
            if param.annotation is not _empty:
                new_annotations[param.name] = param.annotation

    new_func.__signature__ = Signature(parameters=new_params, return_annotation=old_sig.return_annotation)
    new_annotations['return'] = old_sig.return_annotation
    new_func.__annotations__ = new_annotations

    return new_func
