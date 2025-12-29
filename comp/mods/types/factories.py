import re
from typed import factory, Str, TYPE, Tuple

@factory
def Tag(*tags: Tuple(Str)) -> TYPE:
    from comp.mods.types.base    import Jinja

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

    class _Tag(TYPE(Jinja)):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, Str):
                return False
            from comp.mods.helper.helper import _extract_raw_jinja
            jinja = _extract_raw_jinja(instance)
            return bool(tag_regex.match(jinja))
    return _Tag(f'Tag({tags})', (Jinja,), {'__display__': f'Tag({','.join(tags)})'})

@factory
def TAG(tag_name: Str) -> TYPE:
    from comp.mods.helper.types import COMPONENT
    class _TAG(type(COMPONENT)):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, COMPONENT):
                return False
            return issubclass(instance.codomain, Tag(tag_name))
    return _TAG(f'TagComponent({tag_name})', (COMPONENT,), {'__display__': f'TagComponent({tag_name})'})
