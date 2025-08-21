from typed import Str, Bool, Int, Pattern, Union, Enum, Single, Num, Maybe
from typed.models import optional
from comp.models.base import Aria, Globals
from comp.mods.helper.models import _FormEnc, _InputType

@optional
class Input:
    globals:            Globals=Globals()
    aria:               Aria=Aria()
    input_type:         _InputType="text"
    input_id:           Str="input"
    input_class:        Str
    input_placeholder:  Str
    input_name:         Str
    input_autocomplete: Bool
    input_required:     Bool
    input_disabled:     Bool
    input_readonly:     Bool
    input_autofocus:    Bool
    input_tabindex:     Int
    input_form_id:      Str
    input_minlength:    Int
    input_maxlength:    Int
    input_pattern:      Pattern
    input_size:         Int
    input_value:        Str
    input_multiple:     Bool
    input_rows:         Int
    input_cols:         Int
    input_wrap:         Enum(Str, "soft", "hard")
    input_min:          Int
    input_max:          Int
    input_step:         Union(Single("any"), Num)
    input_checked:      Bool
    input_value:        Str

@optional
class Form:
    globals:               Globals=Globals()
    aria:                  Aria=Aria()
    form_id:               Str="form"
    form_class:            Str
    form_style:            Str
    form_name:             Str
    form_action:           Str
    form_method:           Str
    form_enc:              _FormEnc="application/x-www-form-urlencoded"
    form_autocomplete:     Bool
    form_browser_validate: Bool
    form_target:           Str
    form_autofocus:        Bool
    form_charset:          Str="UTF-8"
    form_rel:              Str
