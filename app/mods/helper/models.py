from typed import Enum, Str, Bool, Int, Pattern, List, Extension, Char, Nat
from typed.models import model, Optional
from app.mods.types.base import Inner

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
class Globals:
    anchor: Optional(Str, "")
    accesskey: Optional(Char, " ")
    title: Optional(Str, "")
    tabindex: Optional(Nat, 0)
    hidden: Optional(Bool, False)

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

@model
class Div:
    globals:   Optional(Globals)
    div_id:    Optional(Str, "div")
    div_class: Optional(Str, "")
    div_hover: Optional(Str, "")
    inner:     Optional(Inner, "")

@model
class _FlexSearchTitle:
    title_div:   Optional(Div, Div(div_id="flesearch-results-title-div"))
    title_id:    Optional(Str, "flexsearch-results-title")
    title_class: Optional(Str, "")
    title_hover: Optional(Str, "")

@model
class _FlexSearchDesc:
    desc_div:    Optional(Div, Div(div_id="flesearch-results-desc-div"))
    desc_id:     Optional(Str, "flexsearch-results-desc")
    desc_class:  Optional(Str, "")
    desc_hover:  Optional(Str, "")
    desc_lenght: Optional(Int, 181)
    display:     Optional(Bool, False)

@model
class _FlexSearchCover:
    cover_div:   Optional(Div, Div(div_id="flesearch-results-cover-div"))
    cover_id:    Optional(Str, "flexsearch-results-cover")
    cover_class: Optional(Str, "")
    display:     Optional(Bool, False)

@model
class _FlexSearchKind:
    kind_div:   Optional(Div, Div(div_id="flesearch-results-kind-div"))
    kind_id:    Optional(Str, "flexsearch-results-kind")
    kind_class: Optional(Str, "")
    display:    Optional(Bool, False)

@model
class _FlexSearchResults:
    desc:  _FlexSearchDesc
    title: _FlexSearchTitle
    kind:  _FlexSearchKind
    cover: _FlexSearchCover
    limit: Optional(Int, 10)

@model
class _FlexSearchIndex:
    index_types:       Optional(List(Str), ["title", "content", "tags", "category", "kind"])
    index_store_types: Optional(List(Str), ["id", "title", "content", "href", "tags", "category", "kind"])
    index_json_file:   Optional(Extension('json'), "jsonindex.json")
