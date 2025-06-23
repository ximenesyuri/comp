from typed import typed, Str, Pattern, TypedFuncType, Json

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
    return typed(wrapper)

@typed
def _nill_component(tag_name: Str="") -> Json:
    return {
        "definer": _nill_definer(tag_name)
    }
