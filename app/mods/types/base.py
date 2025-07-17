import re
from typed import Str, Union, Extension
from typed.more import Markdown
from typed.models import Model
from app.mods.types.meta import _Jinja, _Inner, _STATIC
from app.mods.helper.types import (
    COMPONENT,
    _PAGE
)

Jinja   = _Jinja('Jinja', (Str,), {})
Inner   = _Inner('Inner', (Str,), {})
PAGE    = _PAGE('PAGE', (COMPONENT, ), {})
STATIC  = _STATIC('STATIC', (COMPONENT, ), {})
Content = Union(Markdown, Extension('md'))

class STATIC_PAGE:
    pass

Jinja.__display__       = "Jinja"
Inner.__display__       = "Inner"
COMPONENT.__display__   = "COMPONENT"
PAGE.__display__        = "PAGE"
