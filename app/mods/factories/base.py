import re
from typed import factory, Union, Str, List, Int, TYPE, Tuple

@factory
def Tag(*tag_names: Tuple(Str)) -> TYPE:
    from app.mods.types.base    import Jinja
    from app.mods.helper.helper import _jinja_regex
    from app.mods.helper.types  import _nill_jinja

    void_tags = {'input', 'img', 'br', 'hr', 'meta', 'link', 'source', 'track', 'wbr', 'area', 'base', 'col', 'embed', 'param'}

    tags_pattern = "|".join(tag_names)
    if all(tag in void_tags for tag in tag_names):
        pattern_str = rf"^jinja\s*\n?\s*<({tags_pattern})\b[^>]*>(\s*)$"
    else:
        pattern_str = _jinja_regex(tags_pattern)

    tag_regex = re.compile(pattern_str, re.DOTALL)

    class _Tag(type(Jinja)):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, Str):
                return False
            if instance == _nill_jinja:
                return True
            return bool(tag_regex.match(instance))

    return _Tag(f'Tag({tag_names})', (Jinja,), {'__display__': f'Tag({tag_names})'})

@factory
def TagDefiner(tag_name: Str) -> TYPE:
    from app.mods.helper.types import DEFINER
    class _TagDefiner(type(DEFINER)):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, DEFINER):
                return False
            return issubclass(instance.codomain, Tag(tag_name))

    return _TagDefiner(f'TagDefiner({tag_name})', (DEFINER,), {'__display__': f'TagDefiner({tag_name})'})

@factory
def TAG(tag_name: Str) -> TYPE:
    tag_name = str(tag_name)
    TagStrTYPE = Tag(tag_name)
    from app.mods.types.base import COMPONENT

    class _TAG(type(COMPONENT)):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, Component):
                return False
            return isinstance(instance.get("definer"), TagDefiner(tag_name))

    return _TAG(f'TAG({tag_name})', (COMPONENT,), {'__display__': f'TAG({tag_name})'})

@factory
def Definer(*args: Union(Tuple(Str), Tuple(Int))) -> TYPE:
    if len(args) == 0:
        from app.mods.types.base import DEFINER
        return DEFINER
    if len(args) == 1 and isinstance(args[0], int):
        num_vars = args[0]
        if num_vars >= 0:
            processed_vars = num_vars
            type_name = f"Definer({num_vars})"
        else:
            processed_vars = None
            type_name = f"Definer(Any)"
    else:
        processed_vars = frozenset(str(v) for v in args)
        type_name = f"Definer({', '.join(processed_vars)})" if processed_vars else "Definer()"
    from app.mods.types.meta import _Definer
    from app.mods.types.base import DEFINER
    return _Definer(type_name, (DEFINER,), {
        '_free_vars': processed_vars,
        '__display__': type_name
    })
