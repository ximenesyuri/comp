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
from typed.models import model, Optional, Validate, MODEL
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

def _get_jinja(comp):
    if hasattr(comp, "jinja"):
        return comp.jinja
    if hasattr(comp, "_jinja"):
        return comp._jinja
    return ""

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
