import re
from typed import Str, Any, TypedFunc, TypedFuncType
from jinja2 import Environment

class _Jinja(type(Str)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, Str):
            return False

        from app.mods.helper import _jinja_regex
        regex_str = re.compile(_jinja_regex(), re.DOTALL)
        match = regex_str.match(instance)
        if not match:
            return False

        jinja_content = match.group(1)
        try:
            Environment().parse(jinja_content)
            return True
        except Exception as e:
            return False

class _Definer(type(TypedFuncType)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, TypedFuncType):
            return False
        from app.mods.types import Jinja
        return issubclass(instance.codomain, Jinja)

class _FreeDefiner(_Definer):
    def __instancecheck__(cls, instance):
        if not super().__instancecheck__(instance):
            return False
        free_vars_spec = getattr(cls, '_free_vars', frozenset())
        if free_vars_spec is None or (isinstance(free_vars_spec, frozenset) and not free_vars_spec):
            return True
        definer_func = getattr(instance, 'func', instance)
        if not callable(definer_func):
            return False
        from inspect import signature, Parameter
        sig = signature(definer_func)
        definer_params = {p.name for p in sig.parameters.values()}
        call_args = {}
        for name, param in sig.parameters.items():
            if param.default is Parameter.empty:
                call_args[name] = "DUMMY_VALUE_FOR_FREE_CHECK"
        try:
            jinja_str_instance = definer_func(**call_args)
        except Exception:
            return False

        if not isinstance(jinja_str_instance, Str):
            return False

        from app.mods.helper import _find_jinja_vars
        template_variables = _find_jinja_vars(jinja_str_instance)
        effective_free_vars_in_definer = template_variables - definer_params

        if isinstance(free_vars_spec, int):
            return len(effective_free_vars_in_definer) == free_vars_spec
        elif isinstance(free_vars_spec, frozenset):
            for var in free_vars_spec:
                if var in definer_params:
                    return False
                if var not in template_variables:
                    return False
            return True
        return False
