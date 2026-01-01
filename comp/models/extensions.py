from typed import Str, Bool, Dict, Int, List, Union
from utils.types import Json, Extension
from typed.models import optional
from comp.models.base import Globals, Aria
from comp.models.structure import Div
from comp.models.content import Button
from comp.models.form import Input

@optional
class Alpine:
    x_data:       Str
    x_init:       Str
    x_show:       Str
    x_if:         Str
    x_effect:     Str
    x_model:      Str
    x_for:        Str
    x_transition: Str
    x_id:         Str
    x_ref:        Str
    x_cloak:      Bool
    x_bind:       Dict(Str)
    x_on:         Dict(Str)
    x_attrs:      Dict(Str)

Alpine.__display__ = "Alpine"

@optional
class HTMX:
    hx_get:         Str
    hx_post:        Str
    hx_put:         Str
    hx_delete:      Str
    hx_patch:       Str
    hx_target:      Str
    hx_swap:        Str
    hx_trigger:     Str
    hx_confirm:     Str
    hx_include:     Str
    hx_indicator:   Str
    hx_select:      Str
    hx_select_oob:  Str
    hx_ext:         Str
    hx_params:      Str
    hx_vals:        Str
    hx_push_url:    Str
    hx_replace_url: Str
    hx_headers:     Json
    hx_preserve:    Bool
    hx_disable:     Bool
    hx_attrs:       Dict(Str, Json)

HTMX.__display__ = "HTMX"

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
    results_desc:  _SearchDesc=_SearchDesc()
    results_title: _SearchTitle=_SearchTitle()
    results_kind:  _SearchKind=_SearchKind()
    results_cover: _SearchCover=_SearchCover()
    results_limit: Int=10

@optional
class _SearchIndex:
    index_types:       List(Str)=["title", "content", "tags", "category", "kind"]
    index_store_types: List(Str)=["id", "title", "content", "href", "tags", "category", "kind"]
    index_json:        Union(Json, Extension('json'))={}

@optional
class Search:
    search_globals:        Globals
    search_aria:           Aria
    search_div:            Div=Div(div_id="search-div")
    search_input_div:      Div=Div(div_id="search-input-div")
    search_input:          Input=Input(input_type="search", input_id="search-input")
    search_button_div:     Div
    search_button:         Button
    search_results_div:    Div=Div(div_id="search-results-div")
    search_results:        _SearchResults=_SearchResults()
    search_no_results_div: Div=Div(div_id="search-no-results-div")
    search_no_results:     Str="no results..."
    search_index:          _SearchIndex=_SearchIndex()
    search_script:         Str="https://cdn.jsdelivr.net/gh/nextapps-de/searchsearch@0.8.2/dist/searchsearch.bundle.min.js"

Search.__display__ = "Search"
