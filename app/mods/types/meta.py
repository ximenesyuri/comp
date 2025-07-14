import re
from inspect import signature, Parameter, getsource
from typed import Str, Int, Bool, Any, TypedFunc, TypedFuncType, Json
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

class _DEFINER(type(TypedFuncType)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, TypedFuncType):
            return False
        Jinja = _Jinja('Jinja', (Str,), {})
        return issubclass(instance.codomain, Jinja)

class _Definer(_DEFINER):
    def __instancecheck__(cls, instance):
        effective_free_vars_in_definer = instance.jinja_free_vars
        free_vars_spec = getattr(cls, '_free_vars', frozenset())
        if free_vars_spec is None:
            return True
        elif isinstance(free_vars_spec, int):
            result = len(effective_free_vars_in_definer) == free_vars_spec
            return result
        elif isinstance(free_vars_spec, frozenset):
            result = frozenset(effective_free_vars_in_definer) == free_vars_spec
            return result
        return False
