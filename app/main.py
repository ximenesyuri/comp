from app.mods.decorators.base import component, static, page
from app.mods.types.base import *
from app.mods.types.tag  import *
from app.mods.factories.base import *
from app.mods.functions import *
from app.mods.service import *

ALPINE = Script(script_src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js", script_defer=True)
FLEX   = Script(script_src="https://unpkg.com/flexsearch@0.8.2/dist/module/index.js", script_defer=True)
HTMX   = Script(script_src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js", script_defer=True)
