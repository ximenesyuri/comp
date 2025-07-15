from typed import null, PathUrl
from typed.models import model, Optional
from app.mods.decorators.component import component
from app.mods.types.base import *
from app.mods.types.tag  import *
from app.mods.factories.base import *
from app.mods.functions import *
#from app.mods.service import *

@model
class _SCRIPTS:
    alpine: Optional(PathUrl, "https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js")
    htmx: Optional(PathUrl, "https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js")
    flexsearch: Optional(PathUrl, "https://unpkg.com/flexsearch@0.8.2/dist/module/index.js")

SCRIPTS = _SCRIPTS()
