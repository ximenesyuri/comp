from jinja2 import Environment
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

class _Component(type):
    def __instancecheck__(cls, instance):
        return getattr(instance, 'is_component', False)
