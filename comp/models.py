from typed import (
    Int,
    Str,
    Bool,
    List,
    Json,
    Float,
    Maybe,
    Enum,
    Dict,
    HEX,
    Num,
    Union,
    Single,
    Path,
    Url,
    PathUrl,
    null,
    Any,
    Pattern
)
from typed.models import optional
from comp.mods.helper.models import (
    Div,
    Globals,
    _FormEnc,
    _InputType,
    _SearchResults,
    _SearchIndex
)
from comp.mods.types.base import Inner

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
    x_bind:       Dict(Str, Str)
    x_on:         Dict(Str, Str)
    x_attrs:      Dict(Str, Json)

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
class Flex:
    globals:        Globals=Globals()
    flex_id:        Str
    flex_class:     Str="display: flex"
    flex_style:     Str
    flex_direction: Enum(Str, 'row', 'column')

@optional
class Inline:
    globals:      Globals=Globals()
    inline_id:    Str
    inline_class: Str="display: inline"
    inline_style: Str

@optional
class Block:
    globals:      Globals=Globals()
    inline_id:    Str
    inline_class: Str="display: block"
    inline_style: Str

@optional
class Cell:
    globals:      Globals=Globals()
    inline_id:    Str
    inline_class: Str="display: inline"
    inline_style: Str

@optional
class Header:
    globals:      Globals=Globals()
    header_id:    Str="header"
    header_class: Str
    header_style: Str
    header_inner: Any

@optional
class Aside:
    globals:     Globals=Globals()
    aside_id:    Str="aside"
    aside_class: Str
    aside_style: Str
    aside_inner: Any

@optional
class Sidebar:
    globals:       Globals=Globals()
    sidebar_id:    Str="sidebar"
    sidebar_class: Str
    sidebar_style: Str
    sidebar_inner: Any

@optional
class Button:
    globals:      Globals=Globals()
    button_id:    Str="button"
    button_class: Str
    button_style: Str
    button_type:  Enum(Str, "button", "reset", "submmit")="button"
    on_click:     Str
    click_away:   Str
    button_inner: Any

@optional
class Icon:
    icon_id:      Str="icon"
    icon_class:   Str
    icon_size:    Str="24px"
    icon_fill:    HEX="#000000"
    icon_viewbox: Str="0 -960 960 960"
    icon_stroke:  Float=0.5

@optional
class Image:
    globals:   Globals=Globals()
    img_id:    Str="img"
    img_class: Str
    img_style: Str
    img_alt:   Str
    img_src:   PathUrl=""
    img_lazy:  Bool=True
Img = Image

@optional
class Text:
    globals:    Globals=Globals()
    text_id:    Str="text"
    text_class: Str
    text_style: Str
    text_inner: Any

@optional
class Title:
    globals:     Globals=Globals()
    title_id:    Str="title"
    title_class: Str
    title_style: Str
    title_tag:   Enum(Str, "h1", "h2", "h3", "h4", "h5", "h6")="h1"
    title_inner: Any

@optional
class Link:
    globals:       Globals=Globals()
    link_id:       Str="link"
    link_class:    Str
    link_style:    Str
    link_href:     PathUrl="https://"
    link_target:   Enum(Str, "_self", "_blank", "_parent", "_top")="_self"
    link_rel:      Enum(Str, 'nofollow', 'noopener', 'noreferrer', 'sponsored', 'ugc', "")
    link_download: PathUrl
    link_inner:    Any

@optional
class Figure:
    globals:        Globals=Globals()
    figure_img:     Image=Image()
    figure_caption: Str

@optional
class Logo:
    logo_img:  Image=Image()
    logo_link: Link=Link(link_href="/")

@optional
class Item:
    globals:    Globals=Globals()
    item_id:    Str="item"
    item_class: Str
    item_style: Str
    item_inner: Any

@optional
class Unordered:
    globals:  Globals=Globals()
    ul_id:    Str="ul"
    ul_class: Str
    ul_style: Str
    ul_items: List(Item)

@optional
class Ordered:
    globals:  Globals=Globals()
    ol_id:    Str
    ol_class: Str
    ol_style: Str
    ol_items: List(Item)

@optional
class NavItem:
    globals:    Globals=Globals()
    item_id:    Str="item"
    item_class: Str
    item_style: Str
    item_inner: Any
    item_link: Link=Link()

@optional
class Nav:
    globals:       Globals=Globals()
    nav_id:        Str="nav"
    nav_class:     Str
    nav_direction: Enum(Str, "vertical", "horizontal")="horizontal"
    nav_items:     List(NavItem)
    ul_id:         Str="nav-ul"
    ul_class:      Str
    ul_style:      Str="list-style: none;"

@optional
class Script:
    script_src:   Str
    script_defer: Bool
    script_type:  Enum(Str, "module", "importmap")
    script_async: Bool
    script_inner: Any

@optional
class Asset:
    asset_href: Str
    asset_mime: Str
    asset_rel:  Str="stylesheet"

@optional
class Input:
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

@optional
class Search:
    search_div:            Div=Div(div_id="search-div")
    search_input_div:      Div=Div(div_id="search-input-div")
    search_input:          Input=Input(input_type="search", input_id="search-input")
    search_button_div:     Div
    search_button:         Button
    search_results_div:    Div=Div(div_id="search-results-div")
    search_results:        _SearchResults
    search_no_results_div: Div=Div(div_id="search-no-results-div")
    search_no_results:     Str="no results..."
    search_index:          _SearchIndex
    search_script:         Str="https://cdn.jsdelivr.net/gh/nextapps-de/searchsearch@0.8.2/dist/searchsearch.bundle.min.js"
