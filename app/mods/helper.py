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
from app.mods.meta import _Jinja, _Definer

Jinja   = _Jinja('Jinja', (Str,), {})
Content = Union(Markdown, Extension('md'))
Definer = _Definer('Definer', (TypedFuncType,), {})

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

    sig = inspect.signature(getattr(definer, "func", definer))
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

def _jinja_regex(tag_name: Str = "") -> Pattern:
    if tag_name:
        return rf"^jinja\s*\n?\s*<{tag_name}\b[^>]*>(.*?)</{tag_name}>\s*$"
    return r"^jinja\s*\n?\s*(.*?)\s*$"

_nill_jinja  = """jinja """

@typed
def _nill_definer(tag_name: Str="") -> Definer:
    if tag_name:
        from app.mods.factories import TagStr
        def wrapper() -> TagStr(tag_name):
            return _nill_jinja
    else:
        def wrapper() -> Jinja:
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
        # Use the function's name if available, otherwise its string representation
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
        # Handle cases where the definer might not be a simple function
        # (e.g., a class instance with __call__). You might need to
        # inspect differently depending on the structure.
        # For now, raising an error as it indicates an unexpected definer type.
        raise TypeError(
            f"Expected a callable object for definer, but got {final_target_obj!r} "
            f"of type {type(final_target_obj)}"
        )

    sig = inspect.signature(final_target_obj)

    depends_on = []
    if "depends_on" in sig.parameters:
        default = sig.parameters["depends_on"].default
        # Use the default value if it's not inspect.Parameter.empty
        if default is not inspect.Parameter.empty:
            depends_on = default

    # To find undeclared variables in the Jinja template *without* providing values
    # for required parameters, we need to handle the function call carefully.
    # We'll try calling the definer with dummy values only for parameters *without* defaults.
    call_args = {}
    for n, p in sig.parameters.items():
        if n != "depends_on" and p.default is inspect.Parameter.empty:
            # Provide a dummy value for required parameters without defaults
            # This allows the templating to proceed and reveal undeclared variables
            # within the template content.
            # The specific dummy value (like "required_param_placeholder") can be
            # a distinctive string to clearly identify these if they somehow remain
            # in the final template string *before* Jinja parsing.
            call_args[n] = "required_param_placeholder"

    try:
        # If depends_on is a parameter, include it with its (potentially default) value
        if 'depends_on' in sig.parameters:
            jinja = definer(depends_on=depends_on, **call_args)
        else:
            jinja = definer(**call_args)

    except TypeError as e:
         # If the definer call fails with a TypeError despite providing dummy values
         # for non-default params, it might indicate a more complex parameter requirement
         # or an issue with how the typed decorator wraps the function.
         # Re-raise with more context.
         raise TypeError(f"Error calling definer '{getattr(definer, '__name__', str(definer))}' to find Jinja variables: {e}")
    except Exception as e:
        # Catch other potential errors during the definer call.
        print(f"Warning: Could not call definer '{getattr(definer, '__name__', str(definer))}' to find all Jinja variables (might have dynamic requirements): {e}")
        # As a fallback, we'll try calling it without any args, which might miss
        # variables that are only exposed when specific parameters result in different Jinja.
        try:
            if 'depends_on' in sig.parameters:
                # If depends_on has no default and isn't in context, this will likely fail later,
                # but we try to proceed to find other variables.
                jinja = definer(depends_on=depends_on)
            else:
                jinja = definer()
        except Exception:
            # If even calling with defaults or no args fails, we can't reliably get the Jinja.
            # Return empty, but this means missing variables won't be detected.
            return {}


    vars_ = _find_jinja_vars(jinja)
    argnames = set(
        n for n in sig.parameters if n != "depends_on"
    )
    # Variables found in the Jinja template that are NOT among the definer's
    # own parameters (excluding 'depends_on'). These are the variables that
    # must be provided in the context or come from dependencies.
    undeclared_in_definer_params = vars_ - argnames

    result = {}
    for v in undeclared_in_definer_params:
        result[v] = list(path) # Record the path where this variable was found

    # Recursively collect variables from dependencies
    for dep in depends_on:
        if isinstance(dep, Definer):
            dep_name = getattr(dep, "__name__", str(dep))
            result_dep = _get_variables_map(seen.copy(), dep, path + [dep_name])
            result.update(result_dep) # Merge results from dependencies
        else:
            print(f"Warning: Dependency '{dep}' is not a valid Definer and cannot be inspected for variables.")

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
def _check_page(page: Union(_Page, _Static)) -> Bool:
    from app.service import render
    errors = []
    html = render(page)
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
