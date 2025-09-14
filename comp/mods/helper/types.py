import re
from inspect import signature, getsource
from jinja2 import meta
from typed import typed, Str, Dict, Json, Bool, Union, Extension, Path, Typed
from typed.models import model, Optional
from comp.mods.types.meta import _COMPONENT
from comp.mods.helper.helper import _jinja_env

def _has_vars_of_given_type(instance, BASE, typ, n):
    if n < 0:
        return isinstance(instance, BASE)
    count = 0
    ann = getattr(instance, '__annotations__', {})
    for name, t in ann.items():
        try:
            if isinstance(t, type) and (t is typ):
                count += 1
        except Exception:
            pass
    return isinstance(instance, BASE) and count == n

class COMPONENT(_COMPONENT('Component', (Typed,), {})):
    @property
    def jinja(self):
        if hasattr(self, '_jinja'):
            return self._jinja.encode('utf-8').decode('unicode_escape')

        code = getsource(self)
        regex_str = re.compile(r"\"\"\"jinja([\s\S]*?)\"\"\"", re.DOTALL)
        match = regex_str.search(code)
        if match:
            return match.group(1)
        return ""

    def render(self, **context):
        """
        Renders the component into HTML, passing context as variable values.
        """
        from comp.mods.service import render
        return render(self, **context)

    def mock(self, **context):
        """
        Returns a mock PAGE from this component (e.g. using the mock function).
        """
        from comp.mods.service import mock
        return mock(self, **context)

    def preview(self, **context):
        """
        Adds this component to preview stack for interactive viewing.
        """
        from comp.mods.service import preview
        return preview.add(self, **context)

    def __add__(self, other):
        if not isinstance(other, COMPONENT):
            raise TypeError(
                    "Could not realize components 'join' operation:\n"
                f" ==> '{other.__name__}') has wrong type.\n"
                 "     [expected_type] COMPONENT\n"
                f"     [received_type] {type(other).__name__}"
            )
        from comp.mods.functions import join
        return join(self, other)

    def __mul__(self, other):
        if not isinstance(other, COMPONENT):
            raise TypeError(
                "Could not realize components 'concat' operation:\n"
                f" ==> '{other.__name__}' has wrong type.\n"
                 "      [expected_type] COMPONENT\n"
                f"      [received_type] {type(other).__name__}"
            )
        if not isinstance(self, COMPONENT(1)):
            raise TypeError(
                "Could not realize components 'concat' operation:\n"
                f"' ==> {self.__name__}' has wrong type.\n"
                 "      [expected_type] COMPONENT(1)\n"
                f"      [received_type] {type(self).__name__}"
            )

        from comp.mods.functions import concat
        return concat(self, other)

    def __truediv__(self, other):
        if not isinstance(other, dict):
            raise TypeError(
                "Could not realize component 'eval' operation:\n"
                f" ==> '{other}' has wrong type.\n"
                 "     [expected_type] Dict(Any)\n"
                f"     [received_type] {type(other).__name__}"
            )
        if not isinstance(self, COMPONENT):
            raise TypeError(
                "Could not realize component 'eval' operation:\n"
                f" ==> '{self.__name__}' has wrong type.\n"
                 "     [expected_type] COMPONENT\n"
                f"     [received_type] {type(self).__name__}"
            )
        from comp.mods.functions import eval
        return eval(self, **other)

    def __xor__(self, other):
        if not isinstance(other, Dict(Str)):
            raise TypeError(
                "Could not realize component 'copy' operation:\n"
                f" ==> '{other}' has wrong type.\n"
                 "     [expected_type] Dict(Any)\n"
                f"     [received_type] {type(other).__name__}"
            )
        if not isinstance(self, COMPONENT):
            raise TypeError(
                "Could not realize component 'copy' operation:\n"
                f" ==> '{self.__name__}' has wrong type.\n"
                 "     [expected_type] COMPONENT\n"
                f"     [received_type] {type(self).__name__}"
            )
        from comp.mods.functions import copy
        return copy(self, **other)

Content = Union(Str, Extension('md'))

@typed
def _check_page(page: COMPONENT) -> Bool:
    from comp.mods.service import render
    errors = []
    html = render(page)
    html_match = re.search(r"<html[^>]*>(.*?)</html>", html, flags=re.IGNORECASE | re.DOTALL)
    head_match = re.search(r"<head[^>]*>(.*?)</head>", html, flags=re.IGNORECASE | re.DOTALL)
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html, flags=re.IGNORECASE | re.DOTALL)
    if not (html_match and head_match and body_match):
        return False
    html_content = html_match.group(1)
    if not html_content:
        return False
    html_outer_match = re.search(r"<html[^>]*>(.*?)</html>", html, flags=re.IGNORECASE | re.DOTALL)
    head_outer_match = re.search(r"<head[^>]*>(.*?)</head>", html, flags=re.IGNORECASE | re.DOTALL)
    body_outer_match = re.search(r"<body[^>]*>(.*?</body>)", html, flags=re.IGNORECASE | re.DOTALL)

    if not (html_outer_match and head_outer_match and body_outer_match):
        return False
    else:
        html_start, html_end = html_outer_match.span()
        head_start, head_end = head_outer_match.span()
        body_start, body_end = body_outer_match.span()

        if not (html_start < head_start < html_end and head_end < html_end):
            return False
        if not (html_start < body_start < html_end and body_end < html_end):
            return False
        html_opening_tag = re.match(r"<html[^>]*>", html, re.IGNORECASE)
        if html_opening_tag:
            text_before_head = html[html_opening_tag.end():head_start]
            if re.search(r"<[^/!][^>]*>", text_before_head):
                return False
            text_between_head_body = html[head_end:body_start]
            if re.search(r"<[^/!][^>]*>", text_between_head_body):
                return False
        if body_start < head_start < body_end:
            return False
        if head_start < body_start < head_end:
            return False
    return True

class _PAGE(type(COMPONENT)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, COMPONENT):
            return False
        return _check_page(instance)

class _STATIC_PAGE:
    pass
