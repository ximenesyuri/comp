import re
from inspect import signature, Parameter, getsource
from typed import Union, Str, Int, Bool, Any, TypedFunc, TypedFuncType, Json, Prod, Dict
from jinja2 import Environment

class _Jinja(type(Str)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, Union(Str, Prod(Str, Dict(Any)))):
            return False

        from app.mods.helper.helper import _jinja_regex
        regex_str = re.compile(_jinja_regex(), re.DOTALL)
        if isinstance(instance, Str):
            match = regex_str.match(instance)
        else:
            match = regex_str.match(instance[0])
        if not match:
            return False
        jinja_content = match.group(1)
        try:
            Environment().parse(jinja_content)
            return True
        except Exception as e:
            return False

class _COMPONENT(type(TypedFuncType)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, TypedFuncType):
            return False
        return issubclass(instance.codomain, _Jinja('Jinja', (Str,), {}))

class _Component(_COMPONENT):
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

class _Inner(type(str)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, str):
            return False
        return True
