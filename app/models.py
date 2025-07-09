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
    Any
)
from typed.models import Model, Optional, MODEL
from typed.examples import HEX, Num


Alpine = Model(
    x_data=Optional(Json, {}),
    x_init=Optional(Str, ""),
    x_show=Optional(Str, ""),
    x_if=Optional(Str, ""),
    x_effect=Optional(Str, ""),
    x_model=Optional(Str, ""),
    x_for=Optional(Str, ""),
    x_transition=Optional(Str, ""),
    x_id=Optional(Str, ""),
    x_ref=Optional(Str, ""),
    x_cloak=Optional(Bool, False),
    x_bind=Optional(Dict(Str, Str), {}),
    x_on=Optional(Dict(Str, Str), {}),
    x_attrs=Optional(Dict(Str, Json), {}),
)

HTMX = Model(
    hx_get=Optional(Str, ""),
    hx_post=Optional(Str, ""),
    hx_put=Optional(Str, ""),
    hx_delete=Optional(Str, ""),
    hx_patch=Optional(Str, ""),
    hx_target=Optional(Str, ""),
    hx_swap=Optional(Str, ""),
    hx_trigger=Optional(Str, ""),
    hx_confirm=Optional(Str, ""),
    hx_include=Optional(Str, ""),
    hx_indicator=Optional(Str, ""),
    hx_select=Optional(Str, ""),
    hx_select_oob=Optional(Str, ""),
    hx_ext=Optional(Str, ""),
    hx_params=Optional(Str, ""),
    hx_vals=Optional(Str, ""),
    hx_push_url=Optional(Str, ""),
    hx_replace_url=Optional(Str, ""),
    hx_headers=Optional(Json, {}),
    hx_preserve=Optional(Bool, False),
    hx_disable=Optional(Bool, False),
    hx_attrs=Optional(Dict(Str, Json), {})
)

Aria = Model(
    aria_label=Optional(Str, ""),
    aria_labelledby=Optional(Str, ""),
    aria_describedby=Optional(Str, ""),
    aria_controls=Optional(Str, ""),
    aria_current=Optional(Str, ""),
    aria_details=Optional(Str, ""),
    aria_disabled=Optional(Bool, False),
    aria_expanded=Optional(Bool, False),
    aria_hidden=Optional(Bool, False),
    aria_live=Optional(Str, ""),
    aria_pressed=Optional(Str, ""),
    aria_readonly=Optional(Bool, False),
    aria_selected=Optional(Bool, False),
    aria_checked=Optional(Str, ""),
    aria_required=Optional(Bool, False),
    aria_valuemax=Optional(Str, ""),
    aria_valuemin=Optional(Str, ""),
    aria_valuenow=Optional(Str, ""),
    aria_valuetext=Optional(Str, ""),
    aria_role=Optional(Str, ""),
    aria_attrs=Optional(Dict(Str, Str), {})
)

@typed
def _div_factory(name: Str="div") -> MODEL:
    return Model(**{
        f"{name}_id": Optional(Str, f"{name}-div"),
        f"{name}_class": Optional(Str, ""),
        f"{name}_hover": Optional(Str, "")
    })

Div = _div_factory()

Button = Model(
    button_id=Optional(Str, "button"),
    button_class=Optional(Str, ""),
    button_hover=Optional(Str, ""),
    button_type=Optional(Enum(Str, "button", "reset", "submmit"), "button"),
    on_click=Optional(Str, ""),
    click_away=Optional(Str, "")
)

Icon = Model(
    icon_id=Optional(Str, "icon"),
    icon_class=Optional(Str, ""),
    icon_size=Optional(Str, "24px"),
    icon_fill=Optional(HEX, "#000000"),
    icon_viewbox=Optional(Str, "0 -960 960 960"),
    icon_stroke=Optional(Float, 0.5)
)

_input_type_to_model = {
    "text": TextInput,
    "number": NumberInput,
    "email": EmailInput,
    "password": PasswordInput,
    "checkbox": CheckboxInput,
    "radio": RadioInput,
    "file": FileInput,
    "date": DateInput,
    "datetime-local": DatetimeLocalInput,
    "month": MonthInput,
    "week": WeekInput,
    "time": TimeInput,
    "tel": TelInput,
    "url": UrlInput,
    "search": SearchInput,
    "range": RangeInput,
    "color": ColorInput,
    "hidden": HiddenInput,
    "submit": SubmitInput,
    "reset": ResetInput,
    "button": ButtonInput,
    "image": ImageInput,
}

InputType = Enum(Str, *tuple(_input_type_to_model.keys()))

InputBase = Model(
    input_id=Optional(Str, "input"),
    input_class=Optional(Str, ""),
    input_placeholder=Optional(Str, ""),
    input_value=Optional(Str, ""),
    input_name=Optional(Str, ""),
    input_autocomplete=Optional(Bool, False),
    input_required=Optional(Bool, False),
    input_disabled=Optional(Bool, False),
    input_readonly=Optional(Bool, False),
    input_autofocus=Optional(Bool, False),
    input_tabindex=Optional(Int, 0),
    input_form_id=Optional(Str, ""),
)

InputBaseText = Model(
    __extends__=InputBase,
    input_type=Optional(Str, "text"),
    input_minlength=Optional(Int, 0),
    input_maxlength=Optional(Int, 524288),
    input_pattern=Optional(Pattern, r""),
    input_size=Optional(Int, 20)
)

InputText = Model(
    __extends__=InputBaseText,
    input_type=Optional(Str, "text"),
)

InputPassword = Model(
    __extends__=InputBaseText,
    input_type=Optional(Str, "password")
)

InputSearch = Model(
    __extends__=InputBaseText,
    input_type=Optional(Str, "search")
)

InputEmail = Model(
    __extends__=InputBaseText,
    input_type=Optional(InputType, "email"),
    input_multiple=Optional(Bool, False)
)

InputTextArea = Model(
    __extends = InputBase,
    input_rows=Optional(Int, 2),
    input_cols=Optional(Int, 20),
    input_wrap=Optional(Enum(Str, "soft", "hard"), "soft")

)

InputNumber = Model(
    __extends__=Input,
    input_min=Optional(Int, 0),
    input_max=Optional(Int, 0),
    input_step=Optional(Union(Single("any"), Num), ""),
)

InputDate = Model(
    __extends__=Input,
    input_min=Optional(Str, ""),
    input_max=Optional(Str, ""),
    input_step=Optional(Str, ""),
)

InputCheckbox = Model(
    __extends__=Input,
    input_checked=Optional(Bool, False),
    input_value=Optional(Str, "on"),
)


FormEnc = Enum(
    Str,
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain"
)

Form = Model(
    form_id=Optional(Str, "form"),
    form_class=Optional(Str, ""),
    form_hover=Optional(Str, ""),
    form_name=Optional(Str, ""),
    form_action=Optional(Str, ""),          # Submission URL
    form_method=Optional(Str, "get"),       # 'get', 'post', etc.
    form_enc=Optional(FormEnc, "application/x-www-form-urlencoded"),
    form_autocomplete=Optional(Bool, False),
    form_browser_validate=Optional(Bool, False),
    form_target=Optional(Str, ""), # Where to display response
    form_autofocus=Optional(Bool, False),
    form_charset=Optional(Str, "UTF-8"),
    form_rel=Optional(Str, ""),
    form_inputs=Optional(List(InputType), []),
)
