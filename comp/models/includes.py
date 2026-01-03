from typed import Str, Any, Bool, Enum
from typed.models import optional
from comp.models.base import Globals, Aria

@optional
class Script:
    script_globals: Globals
    script_aria:    Aria
    script_src:     Str
    script_defer:   Bool
    script_type:    Enum(Str, "module", "importmap")
    script_async:   Bool
    script_inner:   Any

Script.__display__ = "Script"

@optional
class Asset:
    asset_globals: Globals
    asset_aria:    Aria
    asset_href:    Str
    asset_mime:    Str
    asset_rel:     Str="stylesheet"

Asset.__display__ = "Asset"
