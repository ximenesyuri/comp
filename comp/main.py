from comp.mods.decorators import component, static, page
from comp.mods.types.base import *
from comp.mods.types.tag  import *
from comp.mods.types.factories import *
from comp.mods.functions import *
from comp.mods.service import *

ALPINE = Script(script_src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js", script_defer=True)
FLEX   = Script(script_src="https://cdn.jsdelivr.net/gh/nextcomps-de/flexsearch@0.8.2/dist/flexsearch.bundle.min.js", script_defer=True)
HTMX   = Script(script_src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js", script_defer=True)
