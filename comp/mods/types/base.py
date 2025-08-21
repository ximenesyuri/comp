from typed import Str, Union, Extension
from comp.mods.types.meta import _Jinja, _Inner, _STATIC
from comp.mods.helper.helper import (
    _extract_raw_jinja,
    _find_jinja_inner_vars,
    _find_jinja_vars,
    _render_jinja
)
from comp.mods.helper.types import (
    COMPONENT,
    _PAGE
)

class Jinja(Str, metaclass=_Jinja):
    @property
    def vars(self):
        inner = _find_jinja_inner_vars(_extract_raw_jinja(self))
        all_vars = set(_find_jinja_vars(self))
        free_vars = tuple(sorted(all_vars - set(inner.keys())))
        return {"inner": inner, "free": free_vars}

    @property
    def inner_vars(self):
        return self.vars['inner']

    @property
    def free_vars(self):
        return self.vars['free']

    def render(self, **context):
        return _render_jinja(self, **context)

    __display__ = "Jinja"
    __null__    = "jinja"

Inner   = _Inner('Inner', (Str,), {})
PAGE    = _PAGE('PAGE', (COMPONENT, ), {})
STATIC  = _STATIC('STATIC', (COMPONENT, ), {})
Content = Union(Str, Extension('md'))

class STATIC_PAGE:
    pass

Inner.__display__       = "Inner"
COMPONENT.__display__   = "COMPONENT"
PAGE.__display__        = "PAGE"
