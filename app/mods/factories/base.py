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
            if isinstance(instance, tuple) and len(instance) == 2 and isinstance(instance[0], str):
                instance_str = instance[0]
            else:
                instance_str = instance
            if not isinstance(instance_str, Str):
                return False
            if instance_str == _nill_jinja:
                return True
            return bool(tag_regex.match(instance_str)) 

    return _Tag(f'Tag({tag_names})', (Jinja,), {'__display__': f'Tag({tag_names})'})

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
def Component(*args: Union(Tuple(Str), Tuple(Int))) -> TYPE:
    if len(args) == 0:
        from app.mods.types.base import COMPONENT
        return COMPONENT
    if len(args) == 1 and isinstance(args[0], int):
        num_vars = args[0]
        if num_vars >= 0:
            processed_vars = num_vars
            type_name = f"Component({num_vars})"
        else:
            processed_vars = None
            type_name = f"Component(Any)"
    else:
        processed_vars = frozenset(str(v) for v in args)
        type_name = f"Component({', '.join(processed_vars)})" if processed_vars else "Component()"
    from app.mods.types.meta import _Component
    from app.mods.types.base import COMPONENT
    return _Component(type_name, (COMPONENT,), {
        '_free_vars': processed_vars,
        '__display__': type_name
    })
