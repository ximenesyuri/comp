import re
from inspect import signature, getsource
from jinja2 import meta
from typed import typed, Str, Json, Bool, Union, Extension, Path, TypedFuncType
from typed.models import model, Optional
from typed.more import Markdown
from app.mods.types.meta import _COMPONENT
from app.mods.helper.helper import _jinja_env

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

class COMPONENT(_COMPONENT('Component', (TypedFuncType,), {})):
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

    @property
    def args(self):
        return tuple(signature(self).parameters.keys())

    @property
    def jinja_vars(self):
        env = _jinja_env()
        jinja_content = self.jinja
        if not jinja_content:
            return ()
        ast = env.parse(jinja_content)
        return tuple(sorted(meta.find_undeclared_variables(ast)))

    @property
    def jinja_free_vars(self):
        """Returns the tuple of free Jinja variables (not corresponding to arguments)."""
        all_vars = set(self.jinja_vars)
        arg_vars = set(self.args)
        return tuple(sorted(list(all_vars - arg_vars)))

    def __add__(self, other):
        if not isinstance(other, COMPONENT):
            return NotImplemented
        from app.mods.functions import join
        return join(self, other)

    def __mul__(self, other):
        if not isinstance(other, COMPONENT):
            return NotImplemented
        if not isinstance(self, COMPONENT(1)):
            raise TypeError(
                f"The left operand of '*' (i.e., '{self.__name__}') must be a Definer with "
                "exactly one free Jinja variable to be used with concat (Free(1)).\n"
                f"Its free variables are: {self.jinja_free_vars}"
            )

        from app.mods.functions import concat
        return concat(self, other)

    def __truediv__(self, other):
        if not isinstance(other, dict):
            return NotImplemented
        from app.mods.functions import eval as _eval
        return _eval(self, **other)

Content = Union(Markdown, Extension('md'))

@typed
def _check_page(page: COMPONENT) -> Bool:
    from app.mods.service import render
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
