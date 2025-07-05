from typed import factory, Union, Str, Int, Type, Tuple

@factory
def Tag(tag_name: Str) -> Type:
    from app.mods.helper import Jinja, _jinja_regex, _nill_jinja
    import re

    tag_name = str(tag_name)
    pattern_str = _jinja_regex(tag_name)
    tag_regex = re.compile(pattern_str, re.DOTALL)

    class _Tag(type(Jinja)):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, Str):
                return False
            if instance == _nill_jinja:
                return True
            return bool(tag_regex.match(instance))

    return _Tag(f'Tag({tag_name})', (Jinja,), {'__display__': f'Tag({tag_name})'})

@factory
def TagDefiner(tag_name: Str) -> Type:
    from app.mods.helper import Definer
    class _TagDefiner(type(Definer)):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, Definer):
                return False
            return issubclass(instance.codomain, Tag(tag_name))

    return _TagDefiner(f'TagDefiner({tag_name})', (Definer,), {'__display__': f'TagDefiner({tag_name})'})

@factory
def TAG(tag_name: Str) -> Type:
    tag_name = str(tag_name)
    TagStrType = Tag(tag_name)
    from app.mods.helper import COMPONENT

    class _TAG(type(COMPONENT)):
        def __instancecheck__(cls, instance):
            if not isinstance(instance, Component):
                return False
            return isinstance(instance.get("definer"), TagDefiner(tag_name))

    return _TAG(f'TAG({tag_name})', (COMPONENT,), {'__display__': f'TAG({tag_name})'})


@factory
def Free(*args: Union(Tuple(Str), Tuple(Int))) -> Type:
    if len(args) == 1 and isinstance(args[0], int):
        num_vars = args[0]
        if num_vars >= 0:
            processed_vars = num_vars
            type_name = f"Free({num_vars})"
        else:
            processed_vars = None
            type_name = f"Free(Any)"
    else:
        processed_vars = frozenset(str(v) for v in args)
        type_name = f"Free({', '.join(processed_vars)})" if processed_vars else "Free()"

    from app.mods.meta import _Free
    from app.mods.types import Definer

    return _Free(type_name, (Definer,), {
        '_free_vars': processed_vars,
        '__display__': type_name
    })
