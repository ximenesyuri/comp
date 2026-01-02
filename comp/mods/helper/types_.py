import re
from functools import update_wrapper
from typed import typed, Union, TYPE, Lazy, Str, Dict, Bool, Typed, name
from comp.mods.types.meta import _COMP_, _LAZY_COMP_

def _has_vars_of_given_type(instance, BASE, typ, n):
    if n < 0:
        return instance in BASE
    count = 0
    ann = getattr(instance, '__annotations__', {})
    for name, t in ann.items():
        try:
            if (t in TYPE) and (t is typ):
                count += 1
        except Exception:
            pass
    return (instance in BASE) and count == n

class COMP(Typed, metaclass=_COMP_):
    @property
    def jinja(self):
        if hasattr(self, '_jinja'):
            return self._jinja.encode('utf-8').decode('unicode_escape')
        import inspect
        func = getattr(self, 'func', self)
        while hasattr(func, '__wrapped__'):
            func = func.__wrapped__
        return inspect.getsource(func)

    def render(self, **context):
        from comp.mods.service import render
        return render(self, **context)

    def mock(self, **context):
        from comp.mods.service import mock
        return mock(self, **context)

    def preview(self, **context):
        from comp.mods.service import preview
        return preview.add(self, **context)

    def __add__(self, other):
        if not other in COMP and not other in LAZY_COMP:
            raise TypeError(
                    "Could not realize components 'join' operation:\n"
                f" ==> '{name(other)}') has wrong type.\n"
                 "     [expected_type] COMP or LAZY_COMP\n"
                f"     [received_type] {name(TYPE(other))}"
            )
        from comp.mods.operations import join
        return join(self, other)

    def __mul__(self, other):
        if not other in COMP and not other in LAZY_COMP:
            raise TypeError(
                "Could not realize components 'concat' operation:\n"
                f" ==> '{name(other)}' has wrong type.\n"
                 "      [expected_type] COMP or LAZY_COMP\n"
                f"      [received_type] {name(TYPE(other))}"
            )
        if not self in COMP:
            raise TypeError(
                "Could not realize components 'concat' operation:\n"
                f"' ==> {name(self)}' has wrong type.\n"
                 "      [expected_type] COMP or LAZY_COMP\n"
                f"      [received_type] {name(TYPE(self))}"
            )

        from comp.mods.operations import concat
        return concat(self, other)

    def __truediv__(self, other):
        if other in Dict:
            raise TypeError(
                "Could not realize component 'eval' operation:\n"
                f" ==> '{name(other)}' has wrong type.\n"
                 "     [expected_type] Dict\n"
                f"     [received_type] {name(TYPE(other))}"
            )
        if not self in COMP:
            raise TypeError(
                "Could not realize component 'eval' operation:\n"
                f" ==> '{name(self)}' has wrong type.\n"
                 "     [expected_type] COMP or LAZY_COMP\n"
                f"     [received_type] {name(TYPE(self))}"
            )
        from comp.mods.operations import eval
        return eval(self, **other)

    def __xor__(self, other):
        if not other in Dict(Str):
            raise TypeError(
                "Could not realize component 'copy' operation:\n"
                f" ==> '{name(other)}' has wrong type.\n"
                 "     [expected_type] Dict(Str)\n"
                f"     [received_type] {name(TYPE(other))}"
            )
        if not self in COMP:
            raise TypeError(
                "Could not realize component 'copy' operation:\n"
                f" ==> '{name(self)}' has wrong type.\n"
                 "     [expected_type] COMP\n"
                f"     [received_type] {name(TYPE(self))}"
            )
        from comp.mods.operations import copy
        return copy(self, **other)

    @property
    def __signature__(self):
        import inspect

        func = getattr(self, 'func', None)
        if func is not None:
            return inspect.signature(func)

        call = getattr(type(self), "__call__", None)
        if call is not None and call is not object.__call__:
            return inspect.signature(call)

        return inspect.Signature()

    @property
    def __annotations__(self):
        func = getattr(self, 'func', None)
        if func and hasattr(func, '__annotations__'):
            return func.__annotations__
        return {}

    __display__ = "COMP"

    from comp.mods.helper.null import nill_comp
    __null__ = nill_comp

class LAZY_COMP(Lazy, metaclass=_LAZY_COMP_):
    __display__ = 'LAZY_COMP'
    from comp.mods.helper.null import nill_lazy_comp
    __null__ =  nill_lazy_comp

    def __init__(self, f):
        self._orig = f
        self._wrapped = None
        self.func = f
        self.lazy = True
        self.is_lazy = True
        update_wrapper(self, f)

    def _materialize(self):
        if getattr(self, "_wrapped", None) is None:
            from comp.mods.decorators import comp as _comp
            self._wrapped = _comp(self._orig, lazy=False)
        return self._wrapped

    def __call__(self, *a, **kw):
        return self._materialize()(*a, **kw)

    def __getattr__(self, name_):
        return getattr(self._materialize(), name_)

    def __repr__(self):
        name = getattr(getattr(self, "_orig", None), "__name__", "anonymous")
        return f"<LAZY_COMP for {name}>"

    def __add__(self, other):
        from typed import TYPE, name
        if not (other in COMP or other in LAZY_COMP):
            raise TypeError(
                "Could not realize components 'join' operation:\n"
                f" ==> '{name(other)}') has wrong type.\n"
                "     [expected_type] COMP or LAZY_COMP\n"
                f"     [received_type] {name(TYPE(other))}"
            )
        from comp.mods.operations import join
        return join(self, other)

    def __mul__(self, other):
        from typed import TYPE, name
        if not (other in COMP or other in LAZY_COMP):
            raise TypeError(
                "Could not realize components 'concat' operation:\n"
                f" ==> '{name(other)}' has wrong type.\n"
                "      [expected_type] COMP or LAZY_COMP\n"
                f"      [received_type] {name(TYPE(other))}"
            )
        if not (self in COMP or self in LAZY_COMP):
            raise TypeError(
                "Could not realize components 'concat' operation:\n"
                f"' ==> {name(self)}' has wrong type.\n"
                "      [expected_type] COMP or LAZY_COMP\n"
                f"      [received_type] {name(TYPE(self))}"
            )
        from comp.mods.operations import concat
        return concat(self, other)

    def __truediv__(self, other):
        from typed import TYPE, name, Dict
        if other in Dict:
            raise TypeError(
                "Could not realize component 'eval' operation:\n"
                f" ==> '{name(other)}' has wrong type.\n"
                "     [expected_type] Dict\n"
                f"     [received_type] {name(TYPE(other))}"
            )
        if not (self in COMP or self in LAZY_COMP):
            raise TypeError(
                "Could not realize component 'eval' operation:\n"
                f" ==> '{name(self)}' has wrong type.\n"
                "     [expected_type] COMP or LAZY_COMP\n"
                f"     [received_type] {name(TYPE(self))}"
            )
        from comp.mods.operations import eval
        return eval(self, **other)

    def __xor__(self, other):
        from typed import TYPE, name, Dict, Str
        if not other in Dict(Str):
            raise TypeError(
                "Could not realize component 'copy' operation:\n"
                f" ==> '{name(other)}' has wrong type.\n"
                "     [expected_type] Dict(Str)\n"
                f"     [received_type] {name(TYPE(other))}"
            )
        if not (self in COMP or self in LAZY_COMP):
            raise TypeError(
                "Could not realize component 'copy' operation:\n"
                f" ==> '{name(self)}' has wrong type.\n"
                "     [expected_type] COMP or LAZY_COMP\n"
                f"     [received_type] {name(TYPE(self))}"
            )
        from comp.mods.operations import copy
        return copy(self, **other)

    @property
    def __signature__(self):
        import inspect

        func = getattr(self, 'func', None)
        if func is not None:
            return inspect.signature(func)

        call = getattr(type(self), "__call__", None)
        if call is not None and call is not object.__call__:
            return inspect.signature(call)

        return inspect.Signature()

    @property
    def __annotations__(self):
        func = getattr(self, 'func', None)
        if func and hasattr(func, '__annotations__'):
            return func.__annotations__
        return {}

@typed
def _check_page(page: COMP) -> Bool:
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

class _PAGE(TYPE(COMP), TYPE(LAZY_COMP)):
    def __instancecheck__(cls, instance):
        if not instance in Union(COMP, LAZY_COMP):
            return False
        return _check_page(instance)
