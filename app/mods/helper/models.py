_InputType = Enum(
    Str,
    "text",
    "number",
    "email",
    "password",
    "checkbox",
    "radio",
    "file",
    "date",
    "month",
    "week",
    "time",
    "tel",
    "url",
    "search",
    "range",
    "color",
    "hidden",
    "submit",
    "reset",
    "button",
    "image"
)

@model
class _InputBase:
    input_id:           Optional(Str, "input")
    input_class:        Optional(Str, "")
    input_placeholder:  Optional(Str, "")
    input_name:         Optional(Str, "")
    input_autocomplete: Optional(Bool, False)
    input_required:     Optional(Bool, False)
    input_disabled:     Optional(Bool, False)
    input_readonly:     Optional(Bool, False)
    input_autofocus:    Optional(Bool, False)
    input_tabindex:     Optional(Int, 0)
    input_form_id:      Optional(Str, "")

@model(extends=_InputBase)
class _InputBaseText:
    input_minlength: Optional(Int, 0)
    input_maxlength: Optional(Int, 524288)
    input_pattern:   Optional(Pattern, r"")
    input_size:      Optional(Int, 20)

_FormEnc = Enum(
    Str,
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain"
)
