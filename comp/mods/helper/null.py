from comp.mods.decorators import comp
from comp.mods.types.base import Jinja
from comp.mods.helper.types_ import COMP

def _nill_comp() -> Jinja:
    return """jinja """

COMP.__display__ = "COMP"
COMP.__null__ = comp(_nill_comp)
