from functools import update_wrapper
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

class LAZY_COMP(Lazy, metaclass=_LAZY_COMP_):
    __display__ = 'LAZY_COMP'
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

Responsive = _RESPONSIVE('Responsive', (Typed,), {
    "__display__": "Responsive",
    "__null__": None
})

RESPONSIVE = _RESPONSIVE_('RESPONSIVE', (COMP,), {
    "__display__": "RESPONSIVE",
    "__null__": None
})
