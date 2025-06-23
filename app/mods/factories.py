from typed import belongs, subtype, factory, Str, Any, Type
from app.mods.helper import _jinja_regex, _nill_jinja

@factory
def TagStr(tag_name: Str) -> Type:
    from app.mods.types import JinjaStr
    import re

    tag_name = str(tag_name)
    pattern_str = _jinja_regex(tag_name)
    tag_regex = re.compile(pattern_str, re.DOTALL)

    class _TagStr(type(JinjaStr)):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, Str):
                return False
            if instance == _nill_jinja:
                return True
            return bool(tag_regex.match(instance))

    return _TagStr(f'TagStr({tag_name})', (JinjaStr,), {'__display__': f'TagStr({tag_name})'})

@factory
def TagDefiner(tag_name: Str) -> Type:
    from app.mods.types import Definer
    class _TagDefiner(type(Definer)):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, Definer):
                return False
            return issubclass(instance.codomain, TagStr(tag_name))

    return _TagDefiner(f'TagDefiner({tag_name})', (Definer,), {'__display__': f'TagDefiner({tag_name})'})

@factory
def Tag(tag_name: Str) -> Type:
    tag_name = str(tag_name)
    TagStrType = TagStr(tag_name)
    from app.mods.types import Component

    class _Tag(type(Component)):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, Component):
                return False
            return isinstance(instance.get("definer"), TagDefiner(tag_name))

    return _Tag(f'Tag({tag_name})', (Component,), {'__display__': f'Tag({tag_name})'})

