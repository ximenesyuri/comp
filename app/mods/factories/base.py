import re
from typed import factory, Union, Str, List, Int, TYPE, Tuple

@factory
def Tag(*tags: Tuple(Str)) -> TYPE:
    from app.mods.types.base    import Jinja
    from app.mods.helper.helper import _jinja_regex

    void_tags = {'input', 'img', 'br', 'hr', 'meta', 'link', 'source', 'track', 'wbr', 'area', 'base', 'col', 'embed', 'param'}

    if len(tags) > 1:
        tags_pattern = "|".join(tags)
    else:
        tags_pattern = tags[0]
    if all(tag in void_tags for tag in tuple(tags)):
        pattern_str = rf"^\n?\s*<({tags_pattern})\b[^>]*>(\s*)$"
    else:
        pattern_str = rf"^\n?\s*<{tags_pattern}\b[^>]*>(.*?)</{tags_pattern}>\s*$"

    tag_regex = re.compile(pattern_str, re.DOTALL)

    class _Tag(type(Jinja)):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, Str):
                return False
            from app.mods.helper.helper import _extract_raw_jinja
            jinja = _extract_raw_jinja(instance)
            return bool(tag_regex.match(jinja))
    return _Tag(f'Tag({tags})', (Jinja,), {'__display__': f'Tag({','.join(tags)})'})

@factory
def TAG(tag_name: Str) -> TYPE:
    from app.mods.helper.types import COMPONENT
    class _TAG(type(COMPONENT)):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, COMPONENT):
                return False
            return issubclass(instance.codomain, Tag(tag_name))
    return _TAG(f'TagComponent({tag_name})', (COMPONENT,), {'__display__': f'TagComponent({tag_name})'})

@factory
def Static(*args: Tuple(Int)) -> TYPE:
    from app.mods.types.base import STATIC

    if len(args) == 1:
        name = f'Static({args[0]})'
        if args[0] < 0:
            return STATIC
    elif len(args) == 2:
        name = f'Static({args[0]},{args[1]})'
        if args[1] < 0 and args[0] < 0:
            return STATIC
    else:
        raise ValueError(f"Expected '1' or '2' arguments. Received: '{len(args)} arguments.")

    class _Static(type(STATIC)):
        def __instancecheck__(cls, instance):
            from app.mods.types.base import Inner, Content
            from app.mods.helper.types import _has_vars_of_given_type
            if not isinstance(instance, STATIC):
                return False
            if len(args) == 1:
                return _has_vars_of_given_type(instance, STATIC, Content, args[0])
            if len(args) == 2:
                return  _has_vars_of_given_type(instance, STATIC, Inner, args[0]) and _has_vars_of_given_type(instance, STATIC, Content, args[1])
    return _Static(name, (STATIC,), {'__display__': name})
