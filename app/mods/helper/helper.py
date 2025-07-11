import re
from inspect import signature, Parameter, getsource, isclass
import yaml
from functools import wraps
from typed import (
    typed,
    Str,
    Pattern,
    TypedFuncType,
    Json,
    Bool,
    Extension,
    Set,
    Union,
    Any,
    Path,
    List,
    null,
)
from typed.models import model, conditional, Optional, Instance, MODEL
from typed.more import Markdown
from jinja2 import Environment, meta
from utils import md, file, json, to
from app.mods.decorators.definer import Definer, definer

def _jinja_regex(tag_name: Str = "") -> Pattern:
    if tag_name:
        return rf"^jinja\s*\n?\s*<{tag_name}\b[^>]*>(.*?)</{tag_name}>\s*$"
    return r"^jinja\s*\n?\s*(.*?)\s*$"

def _extract_raw_jinja(jinja_string: Str) -> Str:
    regex_str = re.compile(_jinja_regex(), re.DOTALL)
    match = regex_str.match(jinja_string)
    if match:
        return match.group(1)
    return ""

@typed
def _find_jinja_vars(source: Str) -> Set(Str):
    regex_str = re.compile(_jinja_regex(), re.DOTALL)
    match = regex_str.match(source)
    if not match:
        return set()
    jinja_src = match.group(1)
    env = Environment()
    ast = env.parse(jinja_src)
    return meta.find_undeclared_variables(ast)

@typed
def _get_variables_map(seen: Set(Definer), definer: Definer, path: List(Path)=[]) -> Json:
    if not path:
        path = [getattr(definer, "__name__", str(definer))]

    if definer in seen:
        return {}
    seen.add(definer)

    initial_target_obj = getattr(definer, "func", definer)
    if isinstance(initial_target_obj, tuple) and len(initial_target_obj) == 1:
        final_target_obj = initial_target_obj[0]
    else:
        final_target_obj = initial_target_obj

    if not callable(final_target_obj):
        raise TypeError(
            f"Expected a callable object for definer, but got {final_target_obj!r} "
            f"of type {type(final_target_obj)}"
        )
    sig = signature(final_target_obj)
    depends_on = []
    if "depends_on" in sig.parameters:
        default = sig.parameters["depends_on"].default
        if default is not Parameter.empty:
            depends_on = default

    call_args = {}
    for n, p in sig.parameters.items():
        if n != "depends_on":
            if p.default is Parameter.empty:
                call_args[n] = "required_param_placeholder"
            else:
                call_args[n] = p.default
    try:
        if 'depends_on' in sig.parameters:
            jinja_src = definer(depends_on=depends_on, **call_args)
        else:
            jinja_src = definer(**call_args)
    except Exception:
        jinja_vars = set()
        if hasattr(definer, 'jinja'):
            jinja_str = definer.jinja
            from jinja2 import Environment, meta
            env = Environment()
            try:
                ast = env.parse(jinja_str)
                jinja_vars = meta.find_undeclared_variables(ast)
            except Exception:
                jinja_vars = set()
        jinja_src = ""
    vars_ = set()
    if jinja_src:
        vars_ = _find_jinja_vars(jinja_src)
    argnames = set(n for n in sig.parameters if n != "depends_on")
    undeclared_in_definer_params = vars_ - argnames

    if not jinja_src and hasattr(definer, 'jinja'):
        jinja_str = definer.jinja
        env = Environment()
        try:
            ast = env.parse(jinja_str)
            all_template_vars = meta.find_undeclared_variables(ast)
            undeclared_in_definer_params = set(all_template_vars) - argnames
        except Exception:
            undeclared_in_definer_params = set()
    result = {}
    for v in undeclared_in_definer_params:
        result[v] = list(path)

    for dep in depends_on:
        if isinstance(dep, Definer):
            dep_name = getattr(dep, "__name__", str(dep))
            result_dep = _get_variables_map(seen.copy(), dep, path + [dep_name])
            result.update(result_dep)
        else:
            print(f"Warning: Dependency '{dep}' is not a valid Definer and cannot be inspected for variables.")
    return result

def _make_placeholder_model(param_name, annotation):
    if isinstance(annotation, type) and issubclass(annotation, MODEL):
        fields = getattr(annotation, '__fields__', {})
        field_kwargs = {}
        for fname in fields:
            field_kwargs[fname] = f"{{{{ {param_name}.{fname} }}}}"
        return annotation(field_kwargs)
    else:
        return f"{{{{ {param_name} }}}}"

def _get_annotation(param):
        if param.annotation != Parameter.empty:
            return param.annotation
        elif param.default != Parameter.empty and isinstance(param.default, MODEL):
            return type(param.default)
        else:
            return str
