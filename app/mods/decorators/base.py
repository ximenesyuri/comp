import sys
from inspect import signature, Parameter
from functools import wraps
from typed import typed, List, TypedFuncType
from app.mods.types.base import STATIC

_FREE_COMPONENT_REGISTRY = {}

def _component(arg):
    from app.mods.helper.types import COMPONENT
    """base decorator to create a component"""
    if callable(arg):
        is_dynamic_wrapper = hasattr(arg, '_is_dynamic_component') and \
                             getattr(arg, '_is_dynamic_component') is True

        if not is_dynamic_wrapper:
            original_sig = signature(arg)
            arg.__signature__ = original_sig

        if "depends_on" in signature(arg).parameters:
            param = signature(arg).parameters["depends_on"]
            expected_type_hint = List(COMPONENT)
            if param.annotation is Parameter.empty:
                if not is_dynamic_wrapper:
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

        def local_var_names(fn):
            import dis
            param_names = set(signature(fn).parameters)
            return set(
                instr.argval for instr in dis.get_instructions(fn)
                if instr.opname == "STORE_FAST" and instr.argval not in param_names
            )
        typed_arg = typed(arg)
        from app.mods.helper.types import COMPONENT
        typed_arg.__class__ = COMPONENT
        typed_arg._local_vars = local_var_names(arg)
        from app.mods.types.base import Jinja
        if not issubclass(typed_arg.codomain, Jinja):
            raise TypeError(
                "A component should create a Jinja string:\n"
                f" ==> '{arg.__name__}' codomain is not a subclass of Jinja\n"
                f"     [received_type]: '{typed_arg.codomain.__name__}'"
            )
        if is_dynamic_wrapper:
            if hasattr(arg, '_is_dynamic_component'):
                typed_arg._is_dynamic_component = arg._is_dynamic_component
            if hasattr(arg, '_raw_combined_jinja'):
                typed_arg._raw_combined_jinja = arg._raw_combined_jinja
            if hasattr(arg, '_combined_params_dict'):
                typed_arg._combined_params_dict = arg._combined_params_dict

        @wraps(arg)
        def locals_capture_wrapper(*args, **kwargs):
            frame_container = {}
            def tracer(frame, event, argval):
                if event == "return" and frame.f_code == arg.__code__:
                    frame_container['locals'] = frame.f_locals.copy()
                return tracer
            sys.setprofile(tracer)
            try:
                result = typed_arg(*args, **kwargs)
            finally:
                sys.setprofile(None)
            if (isinstance(result, tuple) and len(result) == 2
                    and isinstance(result[0], str)
                    and isinstance(result[1], dict)):
                return result
            return (result, frame_container.get('locals', {}))

        locals_capture_wrapper.__signature__ = getattr(typed_arg, '__signature__', signature(arg))
        locals_capture_wrapper.__annotations__ = getattr(arg, '__annotations__', {})
        locals_capture_wrapper._local_vars = typed_arg._local_vars
        locals_capture_wrapper._type = COMPONENT
        wrapped = typed(locals_capture_wrapper)
        wrapped.__class__ = COMPONENT
        _FREE_COMPONENT_REGISTRY[arg.__name__] = locals_capture_wrapper
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

def static(comp: STATIC) -> STATIC:
    comp = component(comp)
    if not isinstance(comp, STATIC):
        raise TypeError("The @static decorator can be applied only to functions with at least one argument of type 'Content'.")
