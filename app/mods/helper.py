import re
import inspect
import yaml
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
    null
)
from typed.models import Model, Optional, Instance, Conditional
from typed.examples import Markdown
from jinja2 import Environment, meta
from utils import md, file, json, to
from app.mods.meta import _JinjaStr, _Definer

JinjaStr  = _JinjaStr('JinjaStr', (Str,), {})
Content   = Union(Markdown, Extension('md'))
Definer   = _Definer('Definer', (TypedFuncType,), {})

_Component = Model(
    definer=Definer,
    context=Json
)

@typed
def _check_context(component: _Component) -> Bool:
    definer = component.get('definer')
    context = component.get('context', {})
    if not isinstance(context, dict):
        context = {}
    from inspect import signature
    depends_on = []
    sig = signature(getattr(definer, "func", definer))
    if 'depends_on' in sig.parameters:
        depends_on_default = sig.parameters['depends_on'].default
        depends_on = context.get('depends_on', depends_on_default) or []
    if depends_on is None:
        depends_on = []
    if not isinstance(depends_on, (list, tuple, set)):
        raise TypeError("depends_on must be list, tuple, or set.")
    variables_needed_map = _get_variables_map(set(), definer)
    dep_names = [getattr(dep, '__name__', str(dep)) for dep in depends_on]
    missing = [v for v in variables_needed_map if v not in context and v not in dep_names]
    if not missing:
        return True
    messages = []
    for v in missing:
        trace = " -> ".join(variables_needed_map[v])
        messages.append(f"'{v}' (found in: {trace})")
    message = (
        "The following Jinja variables are not defined in the context:\n"
        + "\n".join(messages)
    )
    raise ValueError(message)

Component = Conditional(
    __conditionals__=_check_context,
    __extends__=_Component
)

_Static = Model(
    __extends__=Component,
    marker=Optional(Str, "content"),
    content=Content,
    frontmatter=Optional(Json, {})
)

@typed
def _check_static_context(static: _Static) -> Bool:
    definer = static.get('definer', _nill_definer())
    marker = static.get('marker', 'content')
    context = static.get('context', {})

    params = set(inspect.signature(definer).parameters)
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

Static = Conditional(
    __conditionals__=[_check_static_context],
    __extends__=_Static
)

@typed
def _jinja_regex(tag_name: Str = "") -> Pattern:
    if tag_name:
        return rf"^jinja\s*\n?\s*<{tag_name}>(.*?)</{tag_name}>\s*$"
    return r"^jinja\s*\n?\s*(.*?)\s*$"

_nill_jinja  = """jinja """

@typed
def _nill_definer(tag_name: Str="") -> Definer:
    if tag_name:
        from app.mods.factories import TagStr
        def wrapper() -> TagStr(tag_name):
            return _nill_jinja
    else:
        def wrapper() -> JinjaStr:
            return _nill_jinja
    return typed(wrapper)

@typed
def _nill_component(tag_name: Str="") -> _Component:
    return {
        "definer": _nill_definer(tag_name),
        "context": {}
    }

@typed
def _nill_static() -> _Static:
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
    initial_target_obj = definer.func if hasattr(definer, "func") else definer

    if isinstance(initial_target_obj, tuple) and len(initial_target_obj) == 1:
        final_target_obj = initial_target_obj[0]
    else:
        final_target_obj = initial_target_obj

    if not callable(final_target_obj):
        raise TypeError(
            f"Expected a callable object, but got {final_target_obj!r} "
            f"of type {type(final_target_obj)}"
        )

    sig = inspect.signature(final_target_obj)

    depends_on = []
    if "depends_on" in sig.parameters:
        default = sig.parameters["depends_on"].default
        if default:
            depends_on = default
    args = []
    for n, p in sig.parameters.items():
        if p.default is inspect.Parameter.empty and n != "depends_on":
            args.append("xxx")
    try:
        jinja = definer(*args)
    except Exception:
        jinja = definer()
    vars_ = _find_jinja_vars(jinja)
    argnames = set(
        n for n in sig.parameters if n != "depends_on"
    )
    undeclared = vars_ - argnames
    result = {v: list(path) for v in undeclared}

    for dep in depends_on:
        dep_name = getattr(dep, "__name__", str(dep))
        result_dep = _get_variables_map(seen, dep, path + [dep_name])
        result.update(result_dep)
    return result

_Page = Model(
    __extends__=Component,
    auto_style=Optional(Bool, False),
    static_dir=Optional(Path, "")
)

_StaticPage = Model(
    __extends__=Static,
    auto_style=Optional(Bool, False),
    static_dir=Optional(Path, "")
)

@typed
def _underlying_component(page: _Page) -> Component:
    return json.rm(
        json_data=page,
        entries=["auto_style", "static_dir"]
    )

@typed
def _underlying_static(page: _StaticPage) -> Static:
    return json.rm(
        json_data=page,
        entries=["auto_style", "static_dir"]
    )

@typed
def _check_page(page: Union(_Page, _Static)) -> Bool:
    if isinstance(page, _Page):
        component = _underlying_component(page)
    else:
        component = _underlying_static(page)
    from app.service import render
    errors = []
    html = render(component)
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


Page = Conditional(
    __conditionals__=[_check_page],
    __extends__=_Page
)

StaticPage = Conditional(
    __conditionals__=[_check_page],
    __extends__=_Static
)
