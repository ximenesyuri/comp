from typed import Str, Any, Bool, Enum
from typed.models import optional
from comp.models.base import Globals, Aria

@optional
class Script:
    globals:      Globals
    aria:         Aria
    script_src:   Str
    script_defer: Bool
    script_type:  Enum(Str, "module", "importmap")
    script_async: Bool
    script_inner: Any

@optional
class Asset:
    globals:    Globals
    aria:       Aria
    asset_href: Str
    asset_mime: Str
    asset_rel:  Str="stylesheet"
