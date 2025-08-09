from typed import Enum, Str, Bool, Int, Pattern, List, Extension, Char, Nat
from typed.models import optional
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

@optional
class Globals:
    anchor:    Str
    accesskey: Char
    title:     Str
    tabindex:  Nat
    hidden:    Bool

_FormEnc = Enum(
    Str,
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain"
)

@optional
class Div:
    globals:   Globals=Globals()
    div_id:    Str
    div_class: Str
    div_style: Str
    div_inner: Inner

@optional
class _FlexTitle:
    title_div:   Div=Div(div_id="flex-results-title-div")
    title_id:    Str="flex-results-title"
    title_class: Str
    title_style: Str

@optional
class _FlexDesc:
    desc_div:    Div=Div(div_id="flex-results-desc-div")
    desc_id:     Str="flex-results-desc"
    desc_class:  Str
    desc_style:  Str
    desc_length: Int=181
    display:     Bool

@optional
class _FlexCover:
    cover_div:   Div=Div(div_id="flex-results-cover-div")
    cover_id:    Str="flex-results-cover"
    cover_class: Str
    cover_style: Str
    display:     Bool

@optional
class _FlexKind:
    kind_div:   Div=Div(div_id="flex-results-kind-div")
    kind_id:    Str="flex-results-kind"
    kind_class: Str
    display:    Bool

@optional
class _FlexResults:
    desc:  _FlexDesc
    title: _FlexTitle
    kind:  _FlexKind
    cover: _FlexCover
    limit: Int=10

@optional
class _FlexIndex:
    index_types:       List(Str)=["title", "content", "tags", "category", "kind"]
    index_store_types: List(Str)=["id", "title", "content", "href", "tags", "category", "kind"]
    index_json_file:   Extension('json')="jsonindex.json"
