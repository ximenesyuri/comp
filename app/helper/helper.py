from typed import typed, Str, Pattern

@typed
def _jinja_regex(tag_name: Str = "") -> Pattern:
    if tag_name:
        return rf"^\s*jinja\s*\n\s*<{tag_name}>(.*?)</{tag_name}>\s*$"
    return rf"^\s*jinja\s*\n(.*?)\s*$"
