from typed import Str, Bool, Dict, Char, Nat
from typed.models import optional

@optional
class Aria:
    aria_label:       Str
    aria_labelledby:  Str
    aria_describedby: Str
    aria_controls:    Str
    aria_current:     Str
    aria_details:     Str
    aria_disabled:    Bool
    aria_expanded:    Bool
    aria_hidden:      Bool
    aria_live:        Str
    aria_pressed:     Str
    aria_readonly:    Bool
    aria_selected:    Bool
    aria_checked:     Str
    aria_required:    Bool
    aria_valuemax:    Str
    aria_valuemin:    Str
    aria_valuenow:    Str
    aria_valuetext:   Str
    aria_role:        Str
    aria_attrs:       Dict(Str, Str)

@optional
class Globals:
    anchor:    Str
    accesskey: Char
    title:     Str
    tabindex:  Nat
    hidden:    Bool
