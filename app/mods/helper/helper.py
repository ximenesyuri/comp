import re
import os
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
from typed.models import model, Optional, Instance, MODEL
from typed.more import Markdown
from jinja2 import Environment, meta, StrictUndefined
from utils import md, file, json, to

_VAR_DELIM = {
    ("[[", "]]"),
    ("<<", ">>"),
    ("((", "))"),
}
_BLOCK_DELIM = {
    ("[%", "%]"),
    ("<%", "%>"),
    ("(%", "%)"),
}
_COMMENT_DELIM = {
    ("[#", "#]"),
    ("(#", "#)"),
    ("<#", "#>"),
}

_DEFAULT_VAR_DELIM = ("[[", "]]")
_DEFAULT_BLOCK_DELIM = ("[%", "%]")
_DEFAULT_COMMENT_DELIM = ("[#", "#]")

def _get_delim(env_var, supported, default):
    v = os.environ.get(env_var, "")
    if v:
        parts = [p.strip() for p in v.split(",", 1)]
        if len(parts) == 2 and (tuple(parts) in supported):
            return tuple(parts)
        raise RuntimeError(
            f"{env_var} must be one of: "
            + ", ".join([f'"{a}, {b}"' for a, b in supported])
        )
    return default

_VAR_DELIM_START, _VAR_DELIM_END = _get_delim("APP_JINJA_VAR_DELIMITERS", _VAR_DELIM, _DEFAULT_VAR_DELIM)
_BLOCK_DELIM_START, _BLOCK_DELIM_END = _get_delim("APP_JINJA_BLOCK_DELIMITERS", _BLOCK_DELIM, _DEFAULT_BLOCK_DELIM)
_COMMENT_DELIM_START, _COMMENT_DELIM_END = _get_delim("APP_JINJA_COMMENT_DELIMITERS", _COMMENT_DELIM, _DEFAULT_COMMENT_DELIM)

_JINJA_DELIM= {
    "variable_start_string": _VAR_DELIM_START,
    "variable_end_string": _VAR_DELIM_END,
    "block_start_string": _BLOCK_DELIM_START,
    "block_end_string": _BLOCK_DELIM_END,
    "comment_start_string": _COMMENT_DELIM_START,
    "comment_end_string": _COMMENT_DELIM_END,
}

_jinja_delim = dict(_JINJA_DELIM)

def _set_jinja_delim(**kwargs):
    _jinja_delim.update(kwargs)

def _jinja_env(undefined=StrictUndefined, **kwargs):
    params = {
        "undefined": undefined,
        **_jinja_delim,
        **kwargs
    }
    return Environment(**params)

def _jinja_regex(tag_name: Str = "") -> Pattern:
    if tag_name:
        return rf"^jinja\s*\n?\s*<{tag_name}\b[^>]*>(.*?)</{tag_name}>\s*$"
    return r"^jinja\s*\n?\s*(.*?)\s*$"

def _extract_raw_jinja(jinja_string: Str) -> Str:
    return re.sub(r"jinja\n?", "", jinja_string) 

@typed
def _find_jinja_vars(source: Str) -> Set(Str):
    regex_str = re.compile(_jinja_regex(), re.DOTALL)
    match = regex_str.match(source)
    if not match:
        return set()
    jinja_src = match.group(1)
    env = _jinja_env()
    ast = env.parse(jinja_src)
    return meta.find_undeclared_variables(ast)

def _get_variables_map(seen, component, path=[]):
    if not path:
        path = [getattr(component, "__name__", str(component))]

    if component in seen:
        return {}
    seen.add(component)

    initial_target_obj = getattr(component, "func", component)
    if isinstance(initial_target_obj, tuple) and len(initial_target_obj) == 1:
        final_target_obj = initial_target_obj[0]
    else:
        final_target_obj = initial_target_obj

    if not callable(final_target_obj):
        raise TypeError(
            f"Expected a callable object for component, but got {final_target_obj!r} "
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
            jinja_src = component(depends_on=depends_on, **call_args)
        else:
            jinja_src = component(**call_args)
    except Exception:
        jinja_vars = set()
        if hasattr(component, 'jinja'):
            jinja_str = component.jinja
            env = _jinja_env()
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
    undeclared_in_component_params = vars_ - argnames

    if not jinja_src and hasattr(component, 'jinja'):
        jinja_str = component.jinja
        env = _jinja_env()
        try:
            ast = env.parse(jinja_str)
            all_template_vars = meta.find_undeclared_variables(ast)
            undeclared_in_component_params = set(all_template_vars) - argnames
        except Exception:
            undeclared_in_component_params = set()
    result = {}
    for v in undeclared_in_component_params:
        result[v] = list(path)

    for dep in depends_on:
        from app.mods.helper.types import COMPONENT
        if isinstance(dep, COMPONENT):
            dep_name = getattr(dep, "__name__", str(dep))
            result_dep = _get_variables_map(seen.copy(), dep, path + [dep_name])
            result.update(result_dep)
        else:
            print(f"Warning: Dependency '{dep}' is not a valid Component and cannot be inspected for variables.")
    return result

def _get_base_name(name):
    m = re.match(r"^(.*?)(?:_\d+)?$", name)
    return m.group(1) if m else name
