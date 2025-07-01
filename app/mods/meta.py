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

class _Free(_Definer):
    def __instancecheck__(cls, instance):
        # 1. isinstance(f, Definer) is True
        if not super().__instancecheck__(instance):
            return False

        # Get the variables passed to Free(*vars)
        free_vars = getattr(cls, '_free_vars', set())

        # If no free variables are specified, any Definer instance passes.
        if not free_vars:
            return True

        # Get the definer's function and its signature
        definer_func = getattr(instance, 'func', instance)
        if not callable(definer_func):
            return False # Should be handled by Definer check, but good to be safe.

        from inspect import signature, Parameter
        sig = signature(definer_func)
        definer_params = {p.name for p in sig.parameters.values()}

        # Get the Jinja string from the definer
        # We need to call the definer to get its Jinja string.
        # Provide dummy values for required parameters to allow the call to succeed
        # and get the template content.
        call_args = {}
        for name, param in sig.parameters.items():
            if param.default is Parameter.empty:
                # Provide a dummy value for required parameters
                call_args[name] = "DUMMY_VALUE_FOR_FREE_CHECK"

        try:
            jinja_str_instance = definer_func(**call_args)
        except Exception:
            # If we can't even get the Jinja string (e.g., due to complex dependencies
            # that dummy values can't satisfy), we can't check its variables.
            return False

        # Ensure the returned value is a Jinja string (already checked by _Definer, but explicit)
        if not isinstance(jinja_str_instance, Str): # Using Str as the base for Jinja is Str
            return False # Or raise a more specific error

        from app.mods.helper import _find_jinja_vars
        template_variables = _find_jinja_vars(jinja_str_instance)

        for var in free_vars:
            # 2. each var in vars is not a variable of "f" (i.e., not a parameter of the definer's function)
            if var in definer_params:
                return False

            # 3. each var in vars is contained in the jinja string of "f" as {{ var }}
            if var not in template_variables:
                return False
        return True
