from typed import typed, Str
from app.mods.types import *
from app.mods.decorators import *
from app.mods.helper import _jinja_regex

@typed
def jinja(jinjastr: Jinja) -> Str:
    import re
    regex_str = re.compile(_jinja_regex(), re.DOTALL)
    match = regex_str.match(jinjastr)
    if match:
        return match.group(1)
    return ""
