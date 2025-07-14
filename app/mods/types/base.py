import re
from typed import Str
from typed.models import Model
from app.mods.types.meta import _Jinja
from app.mods.helper.types import (
    DEFINER,
    COMPONENT,
    STATIC,
    PAGE,
    STATIC_PAGE
)

Jinja   = _Jinja('Jinja', (Str,), {})
Inner = type('Inner', (str,), {})
Context = Model()

Jinja.__display__       = "Jinja"
Inner.__display__       = "Inner"
DEFINER.__display__     = "DEFINER"
COMPONENT.__display__   = "COMPONENT"
STATIC.__display__      = "STATIC"
PAGE.__display__        = "PAGE"
STATIC_PAGE.__display__ = "STATIC_PAGE"
