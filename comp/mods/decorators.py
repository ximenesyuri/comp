import sys
from inspect import signature, Parameter
from functools import wraps
from typed import TYPE, name, typed, Function, Dict, Typed, Any, Union, Str
from comp.mods.types.base import PAGE
from collections import UserList
from types import SimpleNamespace
from inspect import signature, Parameter, isclass, currentframe
from functools import wraps
from comp.mods.helper.types import COMPONENT
from comp.mods.helper.helper import _jinja
from comp.mods.types.base import Jinja

@typed
def jinja(arg: Union(Typed(Any, cod=Str), Str)) -> Jinja:
    if arg in Str:
        return _jinja(arg)
    else:
        if arg.codomain <= Jinja:
            return arg

@typed
def component(arg: Function) -> COMPONENT:
    from comp.mods.helper.types import COMPONENT
    if arg in Function:
        original_sig = signature(arg)
        arg.__signature__ = original_sig

        if "__context__" in signature(arg).parameters:
            param = signature(arg).parameters["__context__"]
            expected_type_hint = Dict
            if param.annotation is Parameter.empty:
                arg.__annotations__["__context__"] = expected_type_hint
            else:
                if param.annotation <= Dict:
                    pass
                else:
                    raise TypeError(
                        f"In a component, argument '__context__' must be of type Dict.\n"
                        f" ==> '{name(arg)}': has '__context__' of wrong type\n"
                        f"     [received_type]: '{name(param.annotation)}'"
                    )

        typed_arg = typed(arg)
        from comp.mods.helper.types import COMPONENT
        typed_arg.__class__ = COMPONENT
        from comp.mods.types.base import Jinja
        if not typed_arg.codomain <= Jinja:
            raise TypeError(
                "A component should create a Jinja string:\n"
                f" ==> '{name(arg)}' codomain is not a subclass of Jinja\n"
                f"     [received_type]: '{name(typed_arg.codomain)}'"
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
            from comp.mods.helper.helper import _jinja_env
            template = _jinja_env().from_string(jinja_src)
            rendered = template.render(**context)
            return _jinja(rendered)

        component_wrapper.__signature__ = getattr(typed_arg, '__signature__', signature(arg))
        component_wrapper.__annotations__ = getattr(arg, '__annotations__', {})
        component_wrapper._type = COMPONENT
        wrapped = typed(component_wrapper)
        wrapped.__class__ = COMPONENT
        return wrapped

    raise TypeError(
        "Component decorator can only be applied to function objects:\n"
        f" ==> '{name(arg)}': is of type Function\n"
        f"     [received_type] '{name(TYPE(arg))}'"
    )

@typed
def page(comp: Function) -> PAGE:
    comp = component(comp)
    return comp
