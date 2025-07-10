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
from typed.models import Model, Optional, Instance, Conditional, MODEL
from typed.more import Markdown
from jinja2 import Environment, meta
from utils import md, file, json, to
from app.mods.definer import Definer
from app.mods.meta import _Jinja

Jinja   = _Jinja('Jinja', (Str,), {})
Content = Union(Markdown, Extension('md'))

_COMPONENT = Model(
    definer=Definer,
    context=Json
)

@typed
def _check_context(component: _COMPONENT) -> Bool:
    definer = component.get('definer')
    context = component.get('context', {})
    if not isinstance(context, dict):
        context = {}

    local_vars = getattr(definer, "_local_vars", set())
    for var in local_vars:
        if var not in context:
            context[var] = ""

    sig = signature(getattr(definer, "func", definer))
    depends_on = []
    if 'depends_on' in sig.parameters:
        depends_on_default = sig.parameters['depends_on'].default
        depends_on = context.get('depends_on', depends_on_default) or []

    if depends_on is None:
        depends_on = []
    if not isinstance(depends_on, (list, tuple, set)):
        raise TypeError("depends_on must be list, tuple, or set.")

    variables_needed_map = _get_variables_map(set(), definer)

    missing = []
    for var_name, trace in variables_needed_map.items():
        if var_name in context:
            continue

        if var_name in sig.parameters and sig.parameters[var_name].default is not inspect.Parameter.empty:
            continue

        is_dependency_name = False
        for dep in depends_on:
            dep_name = getattr(dep, '__name__', str(dep))
            if var_name == dep_name:
                is_dependency_name = True
                break
        if is_dependency_name:
            continue
        missing.append((var_name, trace))
    if not missing:
        return True
    messages = []
    for v, trace in missing:
        messages.append(f"'{v}' (found in: {' -> '.join(trace)})")

    message = (
        "The following Jinja variables are not defined in the context and do not have default values "
        "defined in the definer's signature:\n"
        + "\n".join(messages)
    )
    raise ValueError(message)

COMPONENT = Conditional(
    __conditionals__=_check_context,
    __extends__=_COMPONENT
)

_STATIC = Model(
    __extends__=COMPONENT,
    marker=Optional(Str, "content"),
    content=Content,
    frontmatter=Optional(Json, {})
)

@typed
def _check_static_context(static: _STATIC) -> Bool:
    definer = static.get('definer', _nill_definer())
    marker = static.get('marker', 'content')
    context = static.get('context', {})
    params = set(signature(definer).parameters)
    if marker in params:
        return False
    if marker in context:
        return False
    kwargs = {k: context[k] for k in params if k in context}
    try:
        jinja_str = definer(**kwargs)
    except Exception:
        return False
    pattern = r"\{\{\s*" + re.escape(marker) + r"\s*\}\}"
    found = re.search(pattern, jinja_str) is not None
    return found

STATIC = Conditional(
    __conditionals__=[_check_static_context],
    __extends__=_STATIC
)

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

_nill_jinja  = """jinja """

@typed
def _nill_definer(tag_name: Str="") -> Definer:
    if tag_name:
        from app.mods.factories import Tag
        def wrapper() -> Tag(tag_name):
            return _nill_jinja
    else:
        def wrapper() -> Jinja:
            return _nill_jinja
    from app.mods.definer import _definer
    return _definer(wrapper)

@typed
def _nill_comp(tag_name: Str="") -> _COMPONENT:
    return {
        "definer": _nill_definer(tag_name),
        "context": {}
    }

@typed
def _nill_static() -> _STATIC:
    return {
        "definer": _nill_definer(),
        "context": {},
        "content": ""
    }

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

_PAGE = Model(
    __extends__=COMPONENT,
    auto_style=Optional(Bool, False),
    static_dir=Optional(Path, "")
)

_STATIC_PAGE = Model(
    __extends__=STATIC,
    auto_style=Optional(Bool, False),
    static_dir=Optional(Path, "")
)

@typed
def _check_page_core(page: Union(_PAGE, _STATIC)) -> Bool:
    from app.service import render
    errors = []
    html = render(COMPONENT(page))
    html_match = re.search(r"<html[^>]*>(.*?)</html>", html, flags=re.IGNORECASE | re.DOTALL)
    head_match = re.search(r"<head[^>]*>(.*?)</head>", html, flags=re.IGNORECASE | re.DOTALL)
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html, flags=re.IGNORECASE | re.DOTALL)

    if not html_match:
        errors.append("Missing <html> block.")
    if not head_match:
        errors.append("Missing <head> block.")
    if not body_match:
        errors.append("Missing <body> block.")

    if errors:
        err_text = "\n".join(errors)
        raise AssertionError(f"[check_page] Rendered HTML does not contain required block(s):\n{err_text}\nActual HTML:\n{html[:500]}...")

    html_content = html_match.group(1)

    html_outer_match = re.search(r"<html[^>]*>(.*?)</html>", html, flags=re.IGNORECASE | re.DOTALL)
    head_outer_match = re.search(r"<head[^>]*>(.*?)</head>", html, flags=re.IGNORECASE | re.DOTALL)
    body_outer_match = re.search(r"<body[^>]*>(.*?</body>)", html, flags=re.IGNORECASE | re.DOTALL)

    if not (html_outer_match and head_outer_match and body_outer_match):
        errors.append("One or more essential blocks (html, head, body) could not be located for structural analysis.")
    else:
        html_start, html_end = html_outer_match.span()
        head_start, head_end = head_outer_match.span()
        body_start, body_end = body_outer_match.span()

        if not (html_start < head_start < html_end and head_end < html_end):
            errors.append("<head> block is not contained within <html> block.")
        if not (html_start < body_start < html_end and body_end < html_end):
            errors.append("<body> block is not contained within <html> block.")

        html_opening_tag = re.match(r"<html[^>]*>", html, re.IGNORECASE)
        if html_opening_tag:
            text_before_head = html[html_opening_tag.end():head_start]
            if re.search(r"<[^/!][^>]*>", text_before_head): # Any open tag
                errors.append("<head> block is not a direct child of <html> (other tags found between them).")

            text_between_head_body = html[head_end:body_start]
            if re.search(r"<[^/!][^>]*>", text_between_head_body): # Any open tag
                errors.append("<body> block is not a direct child of <html> (other tags found between <head> and <body>).")
        else:
            errors.append("Could not find <html> opening tag for direct child check.")

        if body_start < head_start < body_end:
            errors.append("<head> block is found inside <body> block.")
        if head_start < body_start < head_end:
            errors.append("<body> block is found inside <head> block.")

    if errors:
        err_text = "\n".join(errors)
        raise AssertionError(f"[check_page] HTML structure validation failed:\n{err_text}\nActual HTML:\n{html[:500]}...")
    return True

@typed
def _check_page(page: _PAGE) -> Bool:
    return _check_page_core(page) and not 'content' in page

@typed
def _check_static_page(page: _STATIC_PAGE) -> Bool:
    return _check_page_core(page) and 'content' in page

PAGE = Conditional(
    __conditionals__=[_check_page],
    __extends__=_PAGE
)

STATIC_PAGE = Conditional(
    __conditionals__=[_check_static_page],
    __extends__=_STATIC_PAGE
)

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
