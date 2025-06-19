from jinja2 import Environment
from typed import type, Str, Any, TypedFunc, TypedFuncType

class __JinjaStr(type(Str)):
    """
    Metaclass for the JinjaStr type.
    Provides instance checking based on basic Jinja syntax parsing.
    """
    def __instancecheck__(cls, instance):
        if not isinstance(instance, Str):
            return False
        try:
            temp_env = Environment()
            temp_env.parse(instance)
            return True
        except Exception as e:
            return False

    def __subclasscheck__(cls, subclass):
        return issubclass(subclass, Str)

class __Component(type(TypedFunc(Any, cod=JinjaStr))):
    """
    Metaclass for the Component type.
    Inherits from the metaclass of TypedFunc(Any, cod=JinjaStr) to facilitate
    subclass and instance checks against that type.

    Provides instance checking to identify objects that are the result of
    applying the @component decorator.
    """

    JinjaStr = __JinjaStr('JinjaStr', (Str,), {})

    def __instancecheck__(cls, instance):
        return isinstance(instance, TypedFunc(Any, cod=JinjaStr)) and getattr(instance, '__is_component__', False)

    def __subclasscheck__(cls, subclass):
        return issubclass(subclass, TypedFunc(Any, cod=JinjaStr))
