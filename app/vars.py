import re
from app.helper.helper import _jinja_regex

JINJA_STR_REGEX = re.compile(_jinja_regex(), re.DOTALL)
