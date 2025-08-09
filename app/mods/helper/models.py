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
    anchor: Optional(Str)
    accesskey: Optional(Char)
    title: Optional(Str)
    tabindex: Optional(Nat)
    hidden: Optional(Bool)

_FormEnc = Enum(
    Str,
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain"
)

@model
class Div:
    globals:   Optional(Globals)
    div_id:    Optional(Str)
    div_class: Optional(Str)
    div_hover: Optional(Str)
    div_inner: Optional(Inner)

@model
class _FlexTitle:
    title_div:   Optional(Div, Div(div_id="flex-results-title-div"))
    title_id:    Optional(Str, "flex-results-title")
    title_class: Optional(Str)
    title_hover: Optional(Str)

@model
class _FlexDesc:
    desc_div:    Optional(Div, Div(div_id="flex-results-desc-div"))
    desc_id:     Optional(Str, "flex-results-desc")
    desc_class:  Optional(Str)
    desc_hover:  Optional(Str)
    desc_length: Optional(Int, 181)
    display:     Optional(Bool)

@model
class _FlexCover:
    cover_div:   Optional(Div, Div(div_id="flex-results-cover-div"))
    cover_id:    Optional(Str, "flex-results-cover")
    cover_class: Optional(Str)
    display:     Optional(Bool)

@model
class _FlexKind:
    kind_div:   Optional(Div, Div(div_id="flex-results-kind-div"))
    kind_id:    Optional(Str, "flex-results-kind")
    kind_class: Optional(Str)
    display:    Optional(Bool)

@model
class _FlexResults:
    desc:  Optional(_FlexDesc)
    title: Optional(_FlexTitle)
    kind:  Optional(_FlexKind)
    cover: Optional(_FlexCover)
    limit: Optional(Int, 10)

@model
class _FlexIndex:
    index_types:       Optional(List(Str), ["title", "content", "tags", "category", "kind"])
    index_store_types: Optional(List(Str), ["id", "title", "content", "href", "tags", "category", "kind"])
    index_json_file:   Optional(Extension('json'), "jsonindex.json")
