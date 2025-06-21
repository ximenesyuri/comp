from jinja2 import Environment
from typed import Str, Any, TypedFunc, TypedFuncType
from app.vars import JINJA_STR_REGEX

class _JinjaStr(type(Str)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, Str):
            return False

        match = JINJA_STR_REGEX.match(instance)
        if not match:
            return False

        jinja_content = match.group(1)

        try:
            Environment().parse(jinja_content)
            return True
        except Exception as e:
            return False

class _Component(type):
    def __instancecheck__(cls, instance):
        return getattr(instance, 'is_component', False)
