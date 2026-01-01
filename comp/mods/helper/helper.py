import re
import os
from jinja2 import meta

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

_VAR_DELIM_START, _VAR_DELIM_END = _get_delim("COMP_JINJA_VAR_DELIM", _VAR_DELIM, _DEFAULT_VAR_DELIM)
_BLOCK_DELIM_START, _BLOCK_DELIM_END = _get_delim("COMP_JINJA_BLOCK_DELIM", _BLOCK_DELIM, _DEFAULT_BLOCK_DELIM)
_COMMENT_DELIM_START, _COMMENT_DELIM_END = _get_delim("COMP_JINJA_COMMENT_DELIM", _COMMENT_DELIM, _DEFAULT_COMMENT_DELIM)

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

_JINJA_ENV_CLS = None
_JINJA_META = None
_JINJA_STRICT = None

def _ensure_jinja():
   global _JINJA_ENV_CLS, _JINJA_META, _JINJA_STRICT
   if _JINJA_ENV_CLS is None:
       from jinja2 import Environment, meta, StrictUndefined
       _JINJA_ENV_CLS, _JINJA_META, _JINJA_STRICT = Environment, meta, StrictUndefined

_env_cache = None

def _jinja_env(undefined=None, **kwargs):
    global _env_cache
    _ensure_jinja()
    if undefined is None:
        undefined = _JINJA_STRICT
    if _env_cache is None and not kwargs:
        _env_cache = _JINJA_ENV_CLS(undefined=undefined, **_jinja_delim)
    if not kwargs:
        return _env_cache
    params = {"undefined": undefined, **_jinja_delim, **kwargs}
    return _JINJA_ENV_CLS(**params)

def _jinja_regex(tag_name=""):
    if tag_name:
        return rf"^jinja\s*\n?\s*<{tag_name}\b[^>]*>(.*?)</{tag_name}>\s*$"
    return r"^jinja\s*\n?\s*(.*?)\s*$"

def _is_jinja(jinja_string, tag_name=""):
    pattern = _jinja_regex(tag_name)
    regex = re.compile(pattern, re.DOTALL)
    return regex.match(jinja_string) is not None

def _extract_raw_jinja(jinja_string):
    return re.sub(r"jinja\n?", "", jinja_string)

def _jinja(string):
    if _is_jinja(string):
        return string
    else:
        return f"""jinja 
{string}"""

def _get_jinja(comp):
    if hasattr(comp, "jinja"):
        return comp.jinja
    if hasattr(comp, "_jinja"):
        return comp._jinja
    return ""

def _find_jinja_vars(source):
    regex_str = re.compile(_jinja_regex(), re.DOTALL)
    match = regex_str.match(source)
    if not match:
        return set()
    jinja_src = match.group(1)
    env = _jinja_env()
    ast = env.parse(jinja_src)
    return meta.find_undeclared_variables(ast)

def _find_jinja_inner_vars(jinja_src, block_start="[%", block_end="%]"):
    inner_vars = {}
    set_pattern = re.compile(
        rf"{re.escape(block_start)}\s*set\s+([a-zA-Z_][\w]*)\s*=\s*(.*?)\s*{re.escape(block_end)}",
        re.DOTALL
    )
    for m in set_pattern.finditer(jinja_src):
        var = m.group(1)
        val = m.group(2)
        val2 = val.strip()
        if val2.startswith('"') and val2.endswith('"'):
            val2 = val2[1:-1]
        elif val2.startswith("'") and val2.endswith("'"):
            val2 = val2[1:-1]
        inner_vars[var] = val2
    return inner_vars

def _render_jinja(jinja_string, **context):
    jinja_src = _extract_raw_jinja(jinja_string)
    env = _jinja_env()
    template = env.from_string(jinja_src)
    return template.render(**context)
