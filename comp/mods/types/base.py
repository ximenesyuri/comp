from typed import Typed, Str, Union, Extension
from comp.mods.types.meta import JINJA, INNER, _RESPONSIVE, _RESPONSIVE_
from comp.mods.helper.types import (
    COMPONENT,
    _PAGE
)
from comp.models.structure import Grid

class Jinja(Str, metaclass=JINJA):
    @property
    def vars(self):
        from comp.mods.service import jinja_vars
        return jinja_vars(self)

    @property
    def inner_vars(self):
        from comp.mods.service import jinja_inner_vars
        return jinja_inner_vars(self)

    @property
    def free_vars(self):
        from comp.mods.service import jinja_free_vars
        return jinja_free_vars(self)

    def render(self, **context):
        from comp.mods.service import render
        return render(self, **context)

    __display__ = "Jinja"
    __null__    = "jinja"

Inner = INNER('Inner', (Str,), {
    "__display__": 'Inner',
    "__null__": ''
})
PAGE = _PAGE('PAGE', (COMPONENT, ), {
    "__display__": 'PAGE',
    "__null__": None
})

GRID = COMPONENT(Grid)
Content = Union(Str, Extension('md'))

Responsive = _RESPONSIVE('Responsive', (Typed,), {
    "__display__": "Responsive",
    "__null__": None
})

RESPONSIVE = _RESPONSIVE_('RESPONSIVE', (COMPONENT,), {
    "__display__": "RESPONSIVE",
    "__null__": None
})

from comp.mods.decorators import component
from comp.mods.types.base import Jinja
def _nill_comp() -> Jinja:
    return """jinja """

COMPONENT.__display__ = "COMPONENT"
COMPONENT.__null__ = component(_nill_comp)
