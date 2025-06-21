import re
from functools import lru_cache

def _jinja_regex(tag_name: str = ""):
    if tag_name:
        return rf"^\s*jinja\n\s*<{tag_name}>.*?</{tag_name}>\s*$"
    return rf"^\s*jinja\n(.*?)\s*$"

class JinjaStr(str):
    pass

@lru_cache(maxsize=None)
def TagStr(tag_name: str):
    tag_name = str(tag_name)
    pattern_str = _jinja_regex(tag_name)
    tag_regex = re.compile(pattern_str, re.DOTALL)

    class _TagStrMeta(type(JinjaStr)):
        def __instancecheck__(cls, instance):
            print("Instancecheck called with repr:", repr(instance))
            if not isinstance(instance, str):
                print("Not a string")
                return False
            result = tag_regex.match(instance) is not None
            print("Regex match:", result)
            return result
        def __subclasscheck__(cls, subclass):
            return issubclass(subclass, JinjaStr)

    return _TagStrMeta(f'TagStr_{tag_name}', (JinjaStr,), {})

tag_str = """jinja
    <tag-name>
        {{aa}}
    </tag-name>
""".strip()

print("REGEX:", _jinja_regex("tag-name"))
print("tag_str repr:", repr(tag_str))
print("regex direct match:", re.match(_jinja_regex("tag-name"), tag_str, re.DOTALL) is not None)
print("isinstance(tag_str, TagStr('tag-name')):",
      isinstance(tag_str, TagStr('tag-name')))
