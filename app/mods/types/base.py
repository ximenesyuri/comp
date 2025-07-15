import re
from typed import Str
from typed.models import Model
from app.mods.types.meta import _Jinja, _Inner
from app.mods.helper.types import (
    COMPONENT,
   # STATIC,
    #PAGE,
    #STATIC_PAGE
)

Jinja   = _Jinja('Jinja', (Str,), {})
Inner = _Inner('Inner', (Str,), {})
Context = Model()

class STATIC:
    pass

class PAGE:
    pass

class STATIC_PAGE:
    pass

Jinja.__display__       = "Jinja"
Inner.__display__       = "Inner"
COMPONENT.__display__   = "COMPONENT"
#STATIC.__display__      = "STATIC"
#PAGE.__display__        = "PAGE"
#STATIC_PAGE.__display__ = "STATIC_PAGE"
