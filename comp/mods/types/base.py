from typed import Typed, Lazy, Str, Union
from utils.types import Extension
from comp.mods.types.meta import JINJA, INNER, _RESPONSIVE, _RESPONSIVE_, _LAZY_COMP_
from comp.mods.helper.types_ import (
    COMP,
    _PAGE
)
from comp.mods.helper.null import nill_lazy_comp

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
PAGE = _PAGE('PAGE', (COMP, ), {
    "__display__": 'PAGE',
    "__null__": None
})

Content = Union(Str, Extension('md'))

LAZY_COMP = _LAZY_COMP_('LAZY_COMP', (Lazy,), {
    "__display__": 'LAZY_COMP',
    "__null__": nill_lazy_comp
})

Responsive = _RESPONSIVE('Responsive', (Typed,), {
    "__display__": "Responsive",
    "__null__": None
})

RESPONSIVE = _RESPONSIVE_('RESPONSIVE', (COMP,), {
    "__display__": "RESPONSIVE",
    "__null__": None
})
