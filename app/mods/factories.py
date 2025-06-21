from functools import lru_cache
from typed import typed, Str, Any, Type
from app.helper.helper import _jinja_regex

@lru_cache(maxsize=None)
@typed
def TagStr(tag_name: str) -> type:
    from app.mods.types import JinjaStr
    import re

    tag_name = str(tag_name)
    pattern_str = _jinja_regex(tag_name)
    tag_regex = re.compile(pattern_str, re.DOTALL)

    class _TagStrMeta(type(JinjaStr)):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, str):
                return False
            return bool(tag_regex.match(instance))

        def __subclasscheck__(cls, subclass):
            return issubclass(subclass, JinjaStr)
    return _TagStrMeta(f'TagStr_{tag_name}', (JinjaStr,), {'__display__': f'TagStr({tag_name})'})

@lru_cache(maxsize=None)
def Tag(tag_name: str) -> type:
    tag_name = str(tag_name)
    TagStrType = TagStr(tag_name)
    from app.mods.types import Component
    class _TagMeta(type(Component)):
        def __instancecheck__(cls, instance):
            return (
                isinstance(instance, Component) and typed(instance).codomain is TagStrType
            )
        def __subclasscheck__(cls, subclass):
            return (
                issubclass(subclass, Component)
            )
    return _TagMeta(
        f'Tag',
        (Component,),
        {'__display__': f'Tag({tag_name})'}
    )
