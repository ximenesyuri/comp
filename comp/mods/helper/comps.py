from typed import typed, Str, Any, Maybe
from comp.models import (
    Div,
    Alpine,
    Text,
    Title,
    Button,
    Link,
    Image,
    Globals,
    Script,
    Figure,
    Asset,
    Item,
    Unordered,
    Ordered,
    Nav,
    Header,
    Aside,
    Sidebar,
    Icon,
    Input,
    Column,
    Row,
    Grid
)

@typed
def if_key(entry: Any = None, what: Str = "") -> Str:
    if entry is not None and entry != "":
        return f' {what}="{entry}"'
    return ""

@typed
def if_bool(entry: Any = None, what: Str = "") -> Str:
    if entry:
        return f" {what}"
    return ""

@typed
def if_size(size: Any = None, key_w: Str = "width", key_h: Str = "height") -> Str:
    if size is not None and size != "":
        return f' {key_w}="{size}" {key_h}="{size}"'
    return ""

@typed
def if_aria(aria: Any = None) -> Str:
    if not aria:
        return ""
    result = ""
    for field, name in [
        ("aria_label",       "aria-label"),
        ("aria_labelledby",  "aria-labelledby"),
        ("aria_describedby", "aria-describedby"),
        ("aria_controls",    "aria-controls"),
        ("aria_current",     "aria-current"),
        ("aria_details",     "aria-details"),
        ("aria_live",        "aria-live"),
        ("aria_pressed",     "aria-pressed"),
        ("aria_checked",     "aria-checked"),
        ("aria_valuemax",    "aria-valuemax"),
        ("aria_valuemin",    "aria-valuemin"),
        ("aria_valuenow",    "aria-valuenow"),
        ("aria_valuetext",   "aria-valuetext"),
    ]:
        val = getattr(aria, field, None)
        if val is not None:
            result += if_key(val, name)
    for field, name in [
        ("aria_disabled", "aria-disabled"),
        ("aria_expanded", "aria-expanded"),
        ("aria_hidden",   "aria-hidden"),
        ("aria_readonly","aria-readonly"),
        ("aria_selected","aria-selected"),
        ("aria_required","aria-required"),
    ]:
        if getattr(aria, field, False):
            result += if_bool(True, name)
    if getattr(aria, "aria_role", None):
        result += if_key(aria.aria_role, "role")
    extra = getattr(aria, "aria_attrs", None)
    if extra:
        for key, val in extra.items():
            if key and val is not None:
                result += f' {key}="{val}"'
    return result

@typed
def if_globals(globals: Maybe(Globals) = None) -> Str:
    if not globals:
        return ""
    return (
        if_key(globals.title,     "title")
      + if_key(globals.tabindex, "tabindex")
      + if_key(globals.accesskey,"accesskey")
      + if_key(globals.anchor,   "anchor")
      + if_bool(globals.hidden,  "hidden")
    )

@typed
def if_id(entry: Any = None) -> Str:
    return if_key(entry, "id")

@typed
def if_class(entry: Any = None) -> Str:
    return if_key(entry, "class")

@typed
def if_style(entry: Any = None) -> Str:
    return if_key(entry, "style")

@typed
def if_div(div: Div = Div()) -> Str:
    if not div:
        return ""
    return (
        if_globals(div.globals)
      + if_aria(div.aria)
      + if_id(div.div_id)
      + if_class(div.div_class)
      + if_style(div.div_style)
    )

@typed
def if_alpine(alpine: Alpine = Alpine()) -> Str:
    if not alpine:
        return ""
    return (
        if_key(alpine.x_init, "x-init")
      + if_key(alpine.x_if,   "x-if")
      + if_key(alpine.x_show, "x-show")
      + if_key(alpine.x_data, "x-data")
      + if_bool(alpine.x_cloak, "x-cloak")
    )

@typed
def if_header(header: Header = Header()) -> Str:
    if not header:
        return ""
    return (
        if_globals(header.globals)
      + if_aria(header.aria)
      + if_id(header.header_id)
      + if_class(header.header_class)
      + if_style(header.header_style)
    )

@typed
def if_aside(aside: Aside = Aside()) -> Str:
    if not aside:
        return ""
    return (
        if_globals(aside.globals)
      + if_aria(aside.aria)
      + if_id(aside.aside_id)
      + if_class(aside.aside_class)
      + if_style(aside.aside_style)
    )

@typed
def if_sidebar(sidebar: Sidebar = Sidebar()) -> Str:
    if not sidebar:
        return ""
    return (
        if_globals(sidebar.globals)
      + if_aria(sidebar.aria)
      + if_id(sidebar.sidebar_id)
      + if_class(sidebar.sidebar_class)
      + if_style(sidebar.sidebar_style)
    )

@typed
def if_col(col: Column=Column()) -> Str:
    if not col:
        return ""
    return (
        if_globals(col.globals)
      + if_aria(col.aria)
      + if_key(col.col_id,    "id")
      + if_key(col.col_class, "class")
      + if_key(col.col_style, "style")
    )

@typed
def if_row(row: Row = Row()) -> Str:
    if not row:
        return ""
    return (
        if_globals(row.globals)
      + if_aria(row.aria)
      + if_key(row.row_id,    "id")
      + if_key(row.row_class, "class")
      + if_key(row.row_style, "style")
    )

@typed
def if_grid(grid: Grid = Grid()) -> Str:
    if not grid:
        return ""
    return (
        if_globals(grid.globals)
      + if_aria(grid.aria)
      + if_key(grid.grid_id,    "id")
      + if_key(grid.grid_class, "class")
      + if_key(grid.grid_style, "style")
    )

@typed
def if_text(text: Text = Text()) -> Str:
    if not text:
        return ""
    return (
        if_globals(text.globals)
      + if_aria(text.aria)
      + if_id(text.text_id)
      + if_class(text.text_class)
      + if_style(text.text_style)
    )

@typed
def if_title(title: Title = Title()) -> Str:
    if not title:
        return ""
    return (
        if_globals(title.globals)
      + if_aria(title.aria)
      + if_id(title.title_id)
      + if_class(title.title_class)
      + if_style(title.title_style)
    )

@typed
def if_link(link: Link = Link()) -> Str:
    if not link:
        return ""
    return (
        if_globals(link.globals)
      + if_aria(link.aria)
      + if_id(link.link_id)
      + if_class(link.link_class)
      + if_style(link.link_style)
      + if_key(link.link_href,     "href")
      + if_key(link.link_download, "download")
      + if_key(link.link_rel,      "rel")
      + if_key(link.link_target,   "target")
    )

@typed
def if_button(button: Button = Button()) -> Str:
    if not button:
        return ""
    return (
        if_globals(button.globals)
      + if_aria(button.aria)
      + if_id(button.button_id)
      + if_class(button.button_class)
      + if_style(button.button_style)
      + if_key(button.on_click,   "@on_click")
      + if_key(button.click_away, "@click_away")
    )

@typed
def if_img(img: Image = Image()) -> Str:
    if not img:
        return ""
    return (
        if_globals(img.globals)
      + if_aria(img.aria)
      + if_id(img.img_id)
      + if_class(img.img_class)
      + if_style(img.img_style)
      + if_key(img.img_lazy, "loading")
      + if_key(img.img_alt,  "alt")
      + if_key(img.img_src,  "src")
    )

@typed
def if_figure(figure: Figure = Figure()) -> Str:
    if not figure:
        return ""
    return (
        if_globals(figure.globals)
      + if_aria(figure.aria)
    )

@typed
def if_script(script: Script = Script()) -> Str:
    if not script:
        return ""
    return (
        if_globals(script.globals)
      + if_aria(script.aria)
      + if_key(script.script_src,  "src")
      + if_key(script.script_type, "type")
      + if_bool(script.script_defer, "defer")
      + if_bool(script.script_async, "async")
    )

@typed
def if_asset(asset: Asset = Asset()) -> Str:
    if not asset:
        return ""
    return (
        if_globals(asset.globals)
      + if_aria(asset.aria)
      + if_key(asset.asset_href, "href")
      + if_key(asset.asset_mime, "type")
      + if_key(asset.asset_rel,  "rel")
    )

@typed
def if_item(item: Item = Item()) -> Str:
    if not item:
        return ""
    return (
        if_globals(item.globals)
      + if_aria(item.aria)
      + if_id(item.item_id)
      + if_class(item.item_class)
      + if_style(item.item_style)
    )

@typed
def if_ul(ul: Unordered = Unordered()) -> Str:
    if not ul:
        return ""
    return (
        if_globals(ul.globals)
      + if_aria(ul.aria)
      + if_id(ul.ul_id)
      + if_class(ul.ul_class)
      + if_style(ul.ul_style)
    )

@typed
def if_ol(ol: Ordered = Ordered()) -> Str:
    if not ol:
        return ""
    return (
        if_globals(ol.globals)
      + if_aria(ol.aria)
      + if_id(ol.ol_id)
      + if_class(ol.ol_class)
      + if_style(ol.ol_style)
    )

@typed
def if_nav(nav: Nav = Nav()) -> Str:
    if not nav:
        return ""
    return (
        if_globals(nav.globals)
      + if_aria(nav.aria)
      + if_id(nav.nav_id)
      + if_class(nav.nav_class)
      + if_style(nav.nav_style)
    )

@typed
def if_icon(icon: Icon = Icon()) -> Str:
    if not icon:
        return ""
    return (
        if_globals(icon.globals)
      + if_id(icon.icon_id)
      + if_class(icon.icon_class)
      + if_style(icon.icon_style)
      + if_key(icon.icon_viewbox, "viewBox")
      + if_size(icon.icon_size)
      + if_key(icon.icon_fill,   "fill")
      + if_key(icon.icon_stroke, "stroke")
      + if_key(getattr(icon, "icon_stroke_width", None), "stroke-width")
    )

@typed
def if_input(input: Input = Input()) -> Str:
    if not input:
        return ""
    return (
        if_globals(input.globals)
      + if_aria(input.aria)
      + if_id(input.input_id)
      + if_class(input.input_class)
      + if_style(input.input_style)
      + if_key(input.input_type,        "type")
      + if_key(input.input_placeholder, "placeholder")
      + if_key(input.input_value,       "value")
      + if_key(input.input_name,        "name")
      + if_key(input.input_autocomplete,"autocomplete")
      + if_bool(input.input_required,   "required")
      + if_bool(input.input_disabled,   "disabled")
      + if_bool(input.input_readonly,   "readonly")
      + if_bool(input.input_autofocus,  "autofocus")
      + if_key(input.input_tabindex,    "tabindex")
      + if_key(input.input_form_id,     "form")
      + if_key(input.input_minlength,   "minlength")
      + if_key(input.input_maxlength,   "maxlength")
      + if_key(input.input_pattern,     "pattern")
      + if_key(input.input_size,        "size")
      + if_key(input.input_min,         "min")
      + if_key(input.input_max,         "max")
      + if_key(input.input_step,        "step")
      + if_bool(input.input_multiple,   "multiple")
      + if_key(getattr(input, "input_accept", None), "accept")
      + if_bool(input.input_checked,    "checked")
      + if_key(getattr(input, "input_for", None),    "for")
    )

