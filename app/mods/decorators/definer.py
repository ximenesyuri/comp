from inspect import signature, Parameter
from functools import wraps
from typed import typed, List, TypedFuncType
from app.mods.types.meta import _Definer

_FREE_DEFINER_REGISTRY = {}

def _definer(arg):
    """base decorator to create a definer"""
    if callable(arg):
        is_dynamic_wrapper = hasattr(arg, '_is_dynamic_definer') and \
                             getattr(arg, '_is_dynamic_definer') is True

        if not is_dynamic_wrapper:
            original_sig = signature(arg)
            arg.__signature__ = original_sig

        if "depends_on" in signature(arg).parameters:
            param = signature(arg).parameters["depends_on"]
            from app.mods.helper.types import DEFINER
            expected_type_hint = List(DEFINER)
            if param.annotation is Parameter.empty:
                if not is_dynamic_wrapper:
                    arg.__annotations__["depends_on"] = expected_type_hint
            else:
                if isclass(param.annotation) and issubclass(param.annotation, List) and \
                   hasattr(param.annotation, '__args__') and param.annotation.__args__ and \
                   issubclass(param.annotation.__args__[0], Definer):
                    pass
                else:
                    raise TypeError(
                        f"In a definer, argument 'depends_on' must be of type List(Definer).\n"
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
        from app.mods.helper.types import DEFINER
        typed_arg.__class__ = DEFINER
        typed_arg._local_vars = local_var_names(arg)
        from app.mods.types.base import Jinja
        if not issubclass(typed_arg.codomain, Jinja):
            raise TypeError(
                "A definer should create a Jinja string:\n"
                f" ==> '{arg.__name__}' codomain is not a subclass of Jinja\n"
                f"     [received_type]: '{typed_arg.codomain.__name__}'"
            )
        if is_dynamic_wrapper:
            if hasattr(arg, '_is_dynamic_definer'):
                typed_arg._is_dynamic_definer = arg._is_dynamic_definer
            if hasattr(arg, '_raw_combined_jinja'):
                typed_arg._raw_combined_jinja = arg._raw_combined_jinja
            if hasattr(arg, '_combined_params_dict'):
                typed_arg._combined_params_dict = arg._combined_params_dict
        res = wraps(arg)(typed_arg)
        _FREE_DEFINER_REGISTRY[arg.__name__] = res
        res._local_vars = typed_arg._local_vars
        return res
    raise TypeError(
        "Definer decorator can only be applied to callable objects:\n"
        f" ==> '{arg.__name__}': is not callable\n"
        f"     [received_type] '{type(arg).__name__}'"
    )

class DefinerProxy:
    def __init__(self, default_decorator):
        self._deco = default_decorator

    def __call__(self, fn):
        return self._deco(fn)

    def __getattr__(self, free_name):
        def proxy(inner_fn):
            free_definer = _FREE_DEFINER_REGISTRY.get(free_name)
            if free_definer is None:
                raise NameError(
                    f"No definer named '{free_name}' registered in _FREE_DEFINER_REGISTRY "
                    f"(needed for '@definer.{free_name}')."
                )
            result_definer = self._deco(inner_fn)
            from app.mods.functions import concat
            return concat(free_definer, result_definer)
        return proxy

definer = DefinerProxy(_definer)
