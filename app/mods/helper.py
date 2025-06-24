from typed import typed, Str, Pattern, TypedFuncType, Json, Bool
import re
import inspect
from jinja2 import Environment, meta

@typed
def _jinja_regex(tag_name: Str = "") -> Pattern:
    if tag_name:
        return rf"^jinja\s*\n?\s*<{tag_name}>(.*?)</{tag_name}>\s*$"
    return r"^jinja\s*\n?\s*(.*?)\s*$"

_nill_jinja  = """jinja """

@typed
def _nill_definer(tag_name: Str="") -> TypedFuncType:
    if tag_name:
        from app.mods.factories import TagStr
        def wrapper() -> TagStr(tag_name):
            return _nill_jinja
    else:
        from app.mods.types import JinjaStr
        def wrapper() -> JinjaStr:
            return _nill_jinja
    from app.mods.comp import definer
    return definer(wrapper)

@typed
def _nill_component(tag_name: Str="") -> Json:
    return {
        "definer": _nill_definer(tag_name)
    }

@typed
def _nill_static() -> Json:
    return {
        "definer": _nill_definer(),
        "content": ""
    }

def _find_jinja_vars(source: str):
    regex_str = re.compile(_jinja_regex(), re.DOTALL)
    match = regex_str.match(source)
    if not match:
        return set()
    jinja_src = match.group(1)
    env = Environment()
    ast = env.parse(jinja_src)
    return meta.find_undeclared_variables(ast)

def _collect_definer_variables_map(definer, path=None, seen=None):
    """
    Recursively collect undeclared jinja variables, mapping variable->path of definers.
    path: stack of definer names for message
    Returns: dict { variable_name: [definer_name, ...] }
    """
    if path is None:
        path = [getattr(definer, "__name__", str(definer))]
    if seen is None:
        seen = set()
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

    try:
        sig = inspect.signature(final_target_obj) 
    except TypeError as e:
        print(f"ERROR: TypeError caught when inspecting signature: {e}")
        print(f"  Problematic target_obj: {target_obj!r}")
        print(f"  Type of problematic target_obj: {type(target_obj)}")
        raise # Re-raise the original error after printing debug info

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
        result_dep = _collect_definer_variables_map(dep, path + [dep_name], seen)
        result.update(result_dep)
    return result
