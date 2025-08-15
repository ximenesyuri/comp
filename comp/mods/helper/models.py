from typed import Enum, Str, Bool, Int, Pattern, List, Extension, Char, Nat
from typed.models import optional
from comp.mods.types.base import Inner

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
class _SearchTitle:
    title_div:   Div=Div(div_id="search-results-title-div")
    title_id:    Str="search-results-title"
    title_class: Str
    title_style: Str

@optional
class _SearchDesc:
    desc_div:    Div=Div(div_id="search-results-desc-div")
    desc_id:     Str="search-results-desc"
    desc_class:  Str
    desc_style:  Str
    desc_length: Int=181
    display:     Bool

@optional
class _SearchCover:
    cover_div:   Div=Div(div_id="search-results-cover-div")
    cover_id:    Str="search-results-cover"
    cover_class: Str
    cover_style: Str
    display:     Bool

@optional
class _SearchKind:
    kind_div:   Div=Div(div_id="search-results-kind-div")
    kind_id:    Str="search-results-kind"
    kind_class: Str
    display:    Bool

@optional
class _SearchResults:
    results_desc:  _SearchDesc
    results_title: _SearchTitle
    results_kind:  _SearchKind
    results_cover: _SearchCover
    results_limit: Int=10

@optional
class _SearchIndex:
    index_types:       List(Str)=["title", "content", "tags", "category", "kind"]
    index_store_types: List(Str)=["id", "title", "content", "href", "tags", "category", "kind"]
    index_json_file:   Extension('json')="jsonindex.json"
