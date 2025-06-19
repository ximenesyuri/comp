from jinja2 import Environment
from typed import Str, Any, TypedFunc, TypedFuncType
from app.vars import JINJA_BLOCK_REGEX

class __JinjaStr(type(Str)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, Str):
            return False

        match = JINJA_BLOCK_REGEX.match(instance)
        if not match:
            return False

        jinja_content = match.group(1)

        try:
            Environment().parse(jinja_content)
            return True
        except Exception as e:
            return False

    def __subclasscheck__(cls, subclass):
        return issubclass(subclass, Str)

class __Component(type(TypedFunc(Any, cod=__JinjaStr('JinjaStr', (Str,), {})))):

    def __instancecheck__(cls, instance):
        return isinstance(instance, TypedFunc(Any, cod=__JinjaStr('JinjaStr', (Str,), {}))) and getattr(instance, '__is_component__', False)

    def __subclasscheck__(cls, subclass):
        return issubclass(subclass, TypedFunc(Any, cod=__JinjaStr('JinjaStr', (Str,), {})))
