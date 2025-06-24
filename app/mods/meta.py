import re
from typed import Str, Any, TypedFunc, TypedFuncType
from jinja2 import Environment
from markdown import markdown
from app.mods.helper import _jinja_regex

class _JinjaStr(type(Str)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, Str):
            return False

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
        from app.mods.types import JinjaStr
        return issubclass(instance.codomain, JinjaStr)

class _Markdown(type(Str)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, Str):
            return False
        try:
            html = markdown(instance)
            return True
        except Exception as e:
            raise TypeError(e)
