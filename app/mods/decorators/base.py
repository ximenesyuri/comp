import sys
from inspect import signature, Parameter
from functools import wraps
from typed import typed, List, TypedFuncType, Function
from app.mods.types.base import STATIC, PAGE, STATIC_PAGE

_FREE_COMPONENT_REGISTRY = {}

def _component(arg):
    from app.mods.helper.types import COMPONENT
    """base decorator to create a component"""
    if callable(arg):
        original_sig = signature(arg)
        arg.__signature__ = original_sig

        if "depends_on" in signature(arg).parameters:
            param = signature(arg).parameters["depends_on"]
            expected_type_hint = List(COMPONENT)
            if param.annotation is Parameter.empty:
                arg.__annotations__["depends_on"] = expected_type_hint
            else:
                if isclass(param.annotation) and issubclass(param.annotation, List) and \
                   hasattr(param.annotation, '__args__') and param.annotation.__args__ and \
                   issubclass(param.annotation.__args__[0], COMPONENT):
                    pass
                else:
                    raise TypeError(
                        f"In a component, argument 'depends_on' must be of type List(Component).\n"
                        f" ==> '{arg.__name__}': has 'depends_on' of wrong type\n"
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

        @wraps(arg)
        def component_wrapper(*args, **kwargs):
            jinja_str = typed_arg(*args, **kwargs)
            import re
            jinja_src = re.sub(r"^jinja\s*\n?", "", jinja_str)
            sig = signature(arg)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            context = bound.arguments
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
        _FREE_COMPONENT_REGISTRY[arg.__name__] = component_wrapper
        return wrapped

    raise TypeError(
        "Component decorator can only be applied to callable objects:\n"
        f" ==> '{arg.__name__}': is not callable\n"
        f"     [received_type] '{type(arg).__name__}'"
    )

class ComponentProxy:
    def __init__(self, default_decorator):
        self._deco = default_decorator

    def __call__(self, fn):
        return self._deco(fn)

    def __getattr__(self, free_name):
        def proxy(inner_fn):
            free_component = _FREE_COMPONENT_REGISTRY.get(free_name)
            if free_component is None:
                raise NameError(
                    f"No component named '{free_name}' registered in _FREE_COMPONENT_REGISTRY "
                    f"(needed for '@component.{free_name}')."
                )
            result_component = self._deco(inner_fn)
            from app.mods.functions import concat
            return concat(free_component, result_component)
        return proxy

component = ComponentProxy(_component)

@typed
def static(comp: Function) -> STATIC:
    comp = component(comp)
    if not isinstance(comp, STATIC):
        raise TypeError("The @static decorator can be applied only to functions with at least one argument of type 'Content'.")
    return comp

@typed
def page(comp: Function) -> PAGE:
    comp = component(comp)
    if not isinstance(comp, PAGE):
        raise TypeError("The @page decorator can be applied only to functions defining a page.")
    return comp

@typed
def static_page(comp: Function) -> STATIC_PAGE:
    comp = component(comp)
    if not isinstance(comp, STATIC_PAGE):
        raise TypeError("The @page decorator can be applied only to functions defining a page.")
    return comp
