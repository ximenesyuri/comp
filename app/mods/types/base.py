import re
from typed import Str
from typed.models import Model
from app.mods.types.meta import _Jinja, _Inner
from app.mods.helper.types import (
    COMPONENT,
    _PAGE
   # STATIC,
    #PAGE,
    #STATIC_PAGE
)

Jinja = _Jinja('Jinja', (Str,), {})
Inner = _Inner('Inner', (Str,), {})
PAGE  = _PAGE('PAGE', (COMPONENT, ), {})

class STATIC:
    pass

class STATIC_PAGE:
    pass

Jinja.__display__       = "Jinja"
Inner.__display__       = "Inner"
COMPONENT.__display__   = "COMPONENT"
PAGE.__display__        = "PAGE"
