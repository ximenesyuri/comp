from typed import (
    typed,
    Int,
    Str,
    Bool,
    List,
    Json,
    Float,
    Maybe,
    Enum,
    Pattern,
    Dict,
    Any,
    HEX,
    Num,
    Union,
    Single
)
from typed.models import model, Optional
from app.mods.helper.models import (
    _FormEnc,
    _InputBase,
    _InputBaseText,
    _InputType
)

@model
class Alpine:
    x_data:       Optional(Json, {})
    x_init:       Optional(Str, "")
    x_show:       Optional(Str, "")
    x_if:         Optional(Str, "")
    x_effect:     Optional(Str, "")
    x_model:      Optional(Str, "")
    x_for:        Optional(Str, "")
    x_transition: Optional(Str, "")
    x_id:         Optional(Str, "")
    x_ref:        Optional(Str, "")
    x_cloak:      Optional(Bool, False)
    x_bind:       Optional(Dict(Str, Str), {})
    x_on:         Optional(Dict(Str, Str), {})
    x_attrs:      Optional(Dict(Str, Json), {})

@model
class HTMX:
    hx_get:         Optional(Str, "")
    hx_post:        Optional(Str, "")
    hx_put:         Optional(Str, "")
    hx_delete:      Optional(Str, "")
    hx_patch:       Optional(Str, "")
    hx_target:      Optional(Str, "")
    hx_swap:        Optional(Str, "")
    hx_trigger:     Optional(Str, "")
    hx_confirm:     Optional(Str, "")
    hx_include:     Optional(Str, "")
    hx_indicator:   Optional(Str, "")
    hx_select:      Optional(Str, "")
    hx_select_oob:  Optional(Str, "")
    hx_ext:         Optional(Str, "")
    hx_params:      Optional(Str, "")
    hx_vals:        Optional(Str, "")
    hx_push_url:    Optional(Str, "")
    hx_replace_url: Optional(Str, "")
    hx_headers:     Optional(Json, {})
    hx_preserve:    Optional(Bool, False)
    hx_disable:     Optional(Bool, False)
    hx_attrs:       Optional(Dict(Str, Json), {})

@model
class Aria:
    aria_label:       Optional(Str, "")
    aria_labelledby:  Optional(Str, "")
    aria_describedby: Optional(Str, "")
    aria_controls:    Optional(Str, "")
    aria_current:     Optional(Str, "")
    aria_details:     Optional(Str, "")
    aria_disabled:    Optional(Bool, False)
    aria_expanded:    Optional(Bool, False)
    aria_hidden:      Optional(Bool, False)
    aria_live:        Optional(Str, "")
    aria_pressed:     Optional(Str, "")
    aria_readonly:    Optional(Bool, False)
    aria_selected:    Optional(Bool, False)
    aria_checked:     Optional(Str, "")
    aria_required:    Optional(Bool, False)
    aria_valuemax:    Optional(Str, "")
    aria_valuemin:    Optional(Str, "")
    aria_valuenow:    Optional(Str, "")
    aria_valuetext:   Optional(Str, "")
    aria_role:        Optional(Str, "")
    aria_attrs:       Optional(Dict(Str, Str), {})

@model
class Div:
    div_id:    Optional(Str, "div")
    div_class: Optional(Str, "")
    div_hover: Optional(Str, "")

@model
class Button:
    button_id:    Optional(Str, "button")
    button_class: Optional(Str, "")
    button_hover: Optional(Str, "")
    button_type:  Optional(Enum(Str, "button", "reset", "submmit"), "button")
    on_click:     Optional(Str, "")
    click_away:   Optional(Str, "")

@model
class Icon:
    icon_id:      Optional(Str, "icon")
    icon_class:   Optional(Str, "")
    icon_size:    Optional(Str, "24px")
    icon_fill:    Optional(HEX, "#000000")
    icon_viewbox: Optional(Str, "0 -960 960 960")
    icon_stroke:  Optional(Float, 0.5)

@model(extends=_InputBaseText)
class InputText:
    input_type: Optional(Str, "text")

@model(extends=_InputBaseText)
class InputPassword:
    input_type: Optional(Str, "password")

@model(extends=_InputBaseText)
class InputSearch:
    input_type: Optional(Str, "search")

@model(extends=_InputBaseText)
class InputEmail:
    input_type:     Optional(InputType, "email")
    input_multiple: Optional(Bool, False)

@model(extends=_InputBase)
class InputTextArea:
    input_rows: Optional(Int, 2)
    input_cols: Optional(Int, 20)
    input_wrap: Optional(Enum(Str, "soft", "hard"), "soft")

@model(extends=_InputBase)
class InputNumber:
    input_min:  Optional(Int, 0)
    input_max:  Optional(Int, 0)
    input_step: Optional(Union(Single("any"), Num), "any")


@model(extends=_InputBase)
class InputDate:
    input_min:  Optional(Str, "")
    input_max:  Optional(Str, "")
    input_step: Optional(Str, "")

@model(extends=_InputBase)
class InputCheckbox:
    input_checked: Optional(Bool, False)
    input_value:   Optional(Str, "on")

@model
class Form:
    form_id: Optional(Str, "form")
    form_class: Optional(Str, "")
    form_hover: Optional(Str, "")
    form_name: Optional(Str, "")
    form_action: Optional(Str, "")
    form_method: Optional(Str, "get")
    form_enc: Optional(_FormEnc, "application/x-www-form-urlencoded")
    form_autocomplete: Optional(Bool, False)
    form_browser_validate: Optional(Bool, False)
    form_target: Optional(Str, "")
    form_autofocus: Optional(Bool, False)
    form_charset: Optional(Str, "UTF-8")
    form_rel: Optional(Str, "")
    form_inputs: Optional(List(InputType), [])

@model
class Image:
    image_id: Optional(Str, "image")
    image_class: Optional(Str, "")
    image_hover: Optional(Str, "")
