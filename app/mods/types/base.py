from typed import Str
from typed.models import Model
from app.mods.decorators.definer import Definer
from app.mods.types.meta import _Jinja
from app.mods.helper.types import (
    COMPONENT,
    STATIC,
    PAGE,
    STATIC_PAGE
)

Jinja   = _Jinja('Jinja', (Str,), {})
Context = Model()

Jinja.__display__       = "Jinja"
Definer.__display__     = "Definer"
COMPONENT.__display__   = "COMPONENT"
STATIC.__display__      = "STATIC"
PAGE.__display__        = "PAGE"
STATIC_PAGE.__display__ = "STATIC_PAGE"
