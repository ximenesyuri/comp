import re
from inspect import signature, Parameter, getsource
from typed import TYPE, Union, Str, Int, Bool, Any, Typed, Json, Prod, Dict
from jinja2 import Environment

class _Jinja(TYPE(Str)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, Str):
            return False

        from comp.mods.helper.helper import _jinja_regex
        regex_str = re.compile(_jinja_regex(), re.DOTALL)
        if isinstance(instance, Str):
            match = regex_str.match(instance)
        if not match:
            return False
        jinja_content = match.group(1)
        try:
            from comp.mods.helper.helper import _jinja_env
            _jinja_env().parse(jinja_content)
            return True
        except Exception as e:
            print(f"{e}")
            return False

class _Inner(TYPE(Str)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, Str):
            return False
        return True

class _COMPONENT(TYPE(Typed)):
    _numbered = {}
    def __call__(cls, *args, **kwargs):
        if not args:
            return super().__call__(cls)
        n = args[0]
        if n not in cls._numbered:
            name = f"COMPONENT({n})"
            from comp.mods.helper.types import COMPONENT
            class _COMPONENT_CALL(COMPONENT):
                _inner_vars = n
                __display__ = name
            cls._numbered[n] = _COMPONENT_CALL
        return cls._numbered[n]

    def __instancecheck__(cls, instance):
        if hasattr(cls, '_inner_vars'):
            from comp.mods.helper.types import COMPONENT, _has_vars_of_given_type
            from comp.mods.types.base import Inner
            return _has_vars_of_given_type(instance, COMPONENT, Inner, cls._inner_vars)
        else:
            return super().__instancecheck__(instance)

def _check_page(page):
    from comp.service import render
    errors = []
    html = render(page)
    html_match = re.search(r"<html[^>]*>(.*?)</html>", html, flags=re.IGNORECASE | re.DOTALL)
    head_match = re.search(r"<head[^>]*>(.*?)</head>", html, flags=re.IGNORECASE | re.DOTALL)
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html, flags=re.IGNORECASE | re.DOTALL)

    if not html_match:
        errors.append("Missing <html> block.")
    if not head_match:
        errors.append("Missing <head> block.")
    if not body_match:
        errors.append("Missing <body> block.")

    if errors:
        err_text = "\n".join(errors)
        raise AssertionError(f"[check_page] Rendered HTML does not contain required block(s):\n{err_text}\nActual HTML:\n{html[:500]}...")

    html_content = html_match.group(1)

    html_outer_match = re.search(r"<html[^>]*>(.*?)</html>", html, flags=re.IGNORECASE | re.DOTALL)
    head_outer_match = re.search(r"<head[^>]*>(.*?)</head>", html, flags=re.IGNORECASE | re.DOTALL)
    body_outer_match = re.search(r"<body[^>]*>(.*?</body>)", html, flags=re.IGNORECASE | re.DOTALL)

    if not (html_outer_match and head_outer_match and body_outer_match):
        errors.append("One or more essential blocks (html, head, body) could not be located for structural analysis.")
    else:
        html_start, html_end = html_outer_match.span()
        head_start, head_end = head_outer_match.span()
        body_start, body_end = body_outer_match.span()

        if not (html_start < head_start < html_end and head_end < html_end):
            errors.append("<head> block is not contained within <html> block.")
        if not (html_start < body_start < html_end and body_end < html_end):
            errors.append("<body> block is not contained within <html> block.")

        html_opening_tag = re.match(r"<html[^>]*>", html, re.IGNORECASE)
        if html_opening_tag:
            text_before_head = html[html_opening_tag.end():head_start]
            if re.search(r"<[^/!][^>]*>", text_before_head): # Any open tag
                errors.append("<head> block is not a direct child of <html> (other tags found between them).")

            text_between_head_body = html[head_end:body_start]
            if re.search(r"<[^/!][^>]*>", text_between_head_body): # Any open tag
                errors.append("<body> block is not a direct child of <html> (other tags found between <head> and <body>).")
        else:
            errors.append("Could not find <html> opening tag for direct child check.")

        if body_start < head_start < body_end:
            errors.append("<head> block is found inside <body> block.")
        if head_start < body_start < head_end:
            errors.append("<body> block is found inside <head> block.")

    if errors:
        err_text = "\n".join(errors)
        raise AssertionError(f"[check_page] HTML structure validation failed:\n{err_text}\nActual HTML:\n{html[:500]}...")
    return True
