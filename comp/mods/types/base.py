from typed import Str, Union, Extension
from comp.mods.types.meta import JINJA, INNER
from comp.mods.helper.types import (
    COMPONENT,
    _PAGE
)

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

Inner   = INNER('Inner', (Str,), {})
PAGE    = _PAGE('PAGE', (COMPONENT, ), {})
Content = Union(Str, Extension('md'))

Inner.__display__       = "Inner"
COMPONENT.__display__   = "COMPONENT"
PAGE.__display__        = "PAGE"
