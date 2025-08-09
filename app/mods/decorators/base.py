import sys
from inspect import signature, Parameter
from functools import wraps
from typed import typed, Function, Dict, Any
from app.mods.types.base import STATIC, PAGE, STATIC_PAGE
from collections import UserList
from types import SimpleNamespace
from inspect import signature, Parameter, isclass, currentframe
from functools import wraps
from app.mods.helper.types import COMPONENT

@typed
def component(arg: Function) -> COMPONENT:
    from app.mods.helper.types import COMPONENT
    if callable(arg):
        original_sig = signature(arg)
        arg.__signature__ = original_sig

        if "__context__" in signature(arg).parameters:
            param = signature(arg).parameters["__context__"]
            expected_type_hint = Dict(Any)
            if param.annotation is Parameter.empty:
                arg.__annotations__["__context__"] = expected_type_hint
            else:
                if issubclass(param.annotation, Dict(Any)):
                    pass
                else:
                    raise TypeError(
                        f"In a component, argument '__context__' must be of type Dict(Any).\n"
                        f" ==> '{arg.__name__}': has '__context__' of wrong type\n"
                        f"     [received_type]: '{param.annotation}'"
                    )

        typed_arg = typed(arg)
        from app.mods.helper.types import COMPONENT
        typed_arg.__class__ = COMPONENT
        from app.mods.types.base import Jinja
        if not issubclass(typed_arg.codomain, Jinja):
            raise TypeError(
                "A component should create a Jinja string:\n"
                f" ==> '{arg.__name__}' codomain is not a subclass of Jinja\n"
                f"     [received_type]: '{typed_arg.codomain.__name__}'"
            )

        func_sig = signature(arg)

        @wraps(arg)
        def component_wrapper(*args, **kwargs):
            if '__context__' in func_sig.parameters:
                param_names = list(func_sig.parameters)
                context_index = param_names.index('__context__')
                if len(args) <= context_index and '__context__' not in kwargs:
                    kwargs['__context__'] = {}

            jinja_str = arg(*args, **kwargs)

            bound = func_sig.bind(*args, **kwargs)
            bound.apply_defaults()
            context = dict(bound.arguments)
            if '__context__' in context and context['__context__']:
                context.update(context['__context__'])

            import re
            jinja_src = re.sub(r"^jinja\s*\n?", "", jinja_str)
            from app.mods.helper.helper import _jinja_env
            template = _jinja_env().from_string(jinja_src)
            rendered = template.render(**context)
            from app.mods.types.base import Jinja
            return Jinja(rendered)

        component_wrapper.__signature__ = getattr(typed_arg, '__signature__', signature(arg))
        component_wrapper.__annotations__ = getattr(arg, '__annotations__', {})
        component_wrapper._type = COMPONENT
        wrapped = typed(component_wrapper)
        wrapped.__class__ = COMPONENT
        return wrapped

    raise TypeError(
        "Component decorator can only be applied to function objects:\n"
        f" ==> '{arg.__name__}': is of type Function\n"
        f"     [received_type] '{type(arg).__name__}'"
    )

@typed
def static(comp: Function) -> STATIC:
    comp = component(comp)
    return comp

@typed
def page(comp: Function) -> PAGE:
    comp = component(comp)
    return comp

@typed
def static_page(comp: Function) -> STATIC_PAGE:
    comp = component(comp)
    return comp

