import re

JINJA_BLOCK_REGEX = re.compile(r'^\s*jinja\n(.*?)\s*$', re.DOTALL)
