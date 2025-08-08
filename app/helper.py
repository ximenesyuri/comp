from typed import typed, Str, Any, Maybe
from app.models import (
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
    _InputBase
)

@typed
def if_key(entry: Any=None, what: Str="id") -> Str:
    if entry and what:
        return f' {what}="{entry}"'
    return ""

@typed
def if_attr(attr: Str="") -> Str:
    if attr:
        return f" {attr}"
    return ""

@typed
def if_globals(globals: Maybe(Globals)=None) -> Str:
    if not globals:
        return ""
    result = ""
    if getattr(globals, 'title', None):
        result += if_key(globals.title, "title")
    if getattr(globals, 'tabindex', None):
        result += if_key(globals.tabindex, "tabindex")
    if getattr(globals, 'accesskey', None):
        result += if_key(globals.accesskey, "accesskey")
    if getattr(globals, 'anchor', None):
        result += if_key(globals.anchor, "anchor")
    if getattr(globals, 'hidden', None):
        if globals.hidden:
            result += if_attr(globals.hidden, "hidden")
    return result

@typed
def if_id(entry: Any=None) -> Str:
    return if_key(entry, "id")

@typed
def if_class(entry: Any=None) -> Str:
    return if_key(entry, "class")

@typed
def if_style(entry: Any=None) -> Str:
    return if_key(entry, "style")

@typed
def if_div(div: Maybe(Div)=None) -> Str:
    if not div:
        return ""
    result = if_globals(getattr(div, 'globals', None))
    result += if_id(getattr(div, 'div_id', None))
    result += if_class(getattr(div, 'div_class', None))
    result += if_style(getattr(div, 'div_style', None))
    return result

@typed
def if_alpine(alpine: Maybe(Alpine)=None) -> Str:
    if not alpine:
        return ""
    result = ""
    if getattr(alpine, 'x_init', None):
        result += if_key(alpine.x_init, "x-init")
    if getattr(alpine, 'x_if', None):
        result += if_key(alpine.x_if, "x-if")
    if getattr(alpine, 'x_show', None):
        result += if_key(alpine.x_show, "x-show")
    if getattr(alpine, 'x_data', None):
        result += if_key(alpine.x_data, "x-data")
    if getattr(alpine, 'x_cloak', None):
        if alpine.x_cloak:
            result += if_attr(alpine.x_cloak, "x-cloak")
    return result

@typed
def if_header(header: Maybe(Header)=None) -> Str:
    if not header:
        return ""
    result = if_globals(getattr(header, 'globals', None))
    result += if_id(getattr(header, 'header_id', None))
    result += if_class(getattr(header, 'header_class', None))
    result += if_style(getattr(header, 'header_style', None))
    return result

@typed
def if_aside(aside: Maybe(Aside)=None) -> Str:
    if not aside:
        return ""
    result = if_globals(getattr(aside, 'globals', None))
    result += if_id(getattr(aside, 'aside_id', None))
    result += if_class(getattr(aside, 'aside_class', None))
    result += if_style(getattr(aside, 'aside_style', None))
    return result

@typed
def if_sidebar(sidebar: Maybe(Sidebar)=None) -> Str:
    if not sidebar:
        return ""
    result = if_globals(getattr(sidebar, 'globals', None))
    result += if_id(getattr(sidebar, 'sidebar_id', None))
    result += if_class(getattr(sidebar, 'sidebar_class', None))
    result += if_style(getattr(sidebar, 'sidebar_style', None))
    return result

@typed
def if_text(text: Maybe(Text)=None) -> Str:
    if not text:
        return ""
    result = if_globals(getattr(text, 'globals', None))
    result += if_id(getattr(text, 'text_id', None))
    result += if_class(getattr(text, 'text_class', None))
    result += if_style(getattr(text, 'text_style', None))
    return result

@typed
def if_title(title: Maybe(Title)=None) -> Str:
    if not title:
        return ""
    result = if_globals(getattr(title, 'globals', None))
    result += if_id(getattr(title, 'title_id', None))
    result += if_class(getattr(title, 'title_class', None))
    result += if_style(getattr(title, 'title_style', None))
    return result

@typed
def if_link(link: Maybe(Link)=None) -> Str:
    if not link:
        return ""
    result = ""
    result += if_globals(getattr(link, 'globals', None))
    result += if_id(getattr(link, 'link_id', None))
    result += if_class(getattr(link, 'link_class', None))
    result += if_style(getattr(link, 'link_style', None))
    if getattr(link, 'link_href', None):
        result += if_key(link.link_href, "href")
    if getattr(link, 'link_download', None):
        result += if_key(link.link_download, "download")
    if getattr(link, 'link_rel', None):
        result += if_key(link.link_rel, "rel")
    if getattr(link, 'link_target', None):
        result += if_key(link.link_target, "target")
    return result

@typed
def if_button(button: Maybe(Button)=None) -> Str:
    if not button:
        return ""
    result = if_globals(getattr(button, 'globals', None))
    result += if_id(getattr(button, 'button_id', None))
    result += if_class(getattr(button, 'button_class', None))
    result += if_style(getattr(button, 'button_style', None))
    if getattr(button, 'on_click', None):
        result += if_key(button.on_click, "@on_click")
    if getattr(button, 'click_away', None):
        result += if_key(button.click_away, "@click_away")
    return result

@typed
def if_img(img: Maybe(Image)=None) -> Str:
    if not img:
        return ""
    result = if_globals(getattr(img, 'globals', None))
    result += if_id(getattr(img, 'img_id', None))
    result += if_class(getattr(img, 'img_class', None))
    result += if_style(getattr(img, 'img_style', None))
    if getattr(img, 'img_lazy', None):
        result += if_key(img.img_lazy, "loading")
    if getattr(img, 'img_alt', None):
        result += if_key(img.img_alt, "alt")
    if getattr(img, 'img_src', None):
        result += if_key(img.img_src, "src")
    return result

@typed
def if_figure(figure: Maybe(Figure)=None) -> Str:
    if not figure:
        return ""
    return if_globals(getattr(figure, 'globals', None))

@typed
def if_script(script: Script=None) -> Str:
    if not script:
        return ""
    result = ""
    if getattr(script, 'script_src', None):
        result += if_key(script.script_src, "src")
    if getattr(script, 'script_type', None):
        result += if_key(script.script_type, "type")
    if getattr(script, 'script_defer', None) and script.script_defer:
        result += if_attr(script.script_defer, "defer")
    if getattr(script, 'script_async', None) and script.script_async:
        result += if_attr(script.script_async, "async")
    return result

@typed
def if_asset(asset: Maybe(Asset)=None) -> Str:
    if not asset:
        return ""
    result = ""
    if getattr(asset, 'asset_href', None):
        result += if_key(asset.asset_href, "href")
    if getattr(asset, 'asset_mime', None):
        result += if_key(asset.asset_mime, "type")
    if getattr(asset, 'asset_rel', None):
        result += if_key(asset.asset_rel, "rel")
    return result

@typed
def if_item(item: Maybe(Item)=None) -> str:
    if not item:
        return ""
    result = if_id(getattr(item, 'item_id', None))
    result += if_class(getattr(item, 'item_class', None))
    result += if_style(getattr(item, 'item_style', None))
    return result

@typed
def if_ul(ul: Maybe(Unordered)=None) -> str:
    if not ul:
        return ""
    result = if_id(getattr(ul, 'ul_id', None))
    result += if_class(getattr(ul, 'ul_class', None))
    result += if_style(getattr(ul, 'ul_style', None))
    return result

@typed
def if_ol(ol: Maybe(Ordered)=None) -> str:
    if not ol:
        return ""
    result = if_id(getattr(ol, 'ol_id', None))
    result += if_class(getattr(ol, 'ol_class', None))
    result += if_style(getattr(ol, 'ol_style', None))
    return result

@typed
def if_nav(nav: Maybe(Nav)=None) -> str:
    if not nav:
        return ""
    result = if_id(getattr(nav, 'nav_id', None))
    result += if_class(getattr(nav, 'nav_class', None))
    result += if_style(getattr(nav, 'nav_style', None))
    return result

@typed
def if_icon(icon: Maybe(Icon)=None) -> Str:
    if not icon:
        return ""
    result = ""
    result += if_globals(getattr(icon, 'globals', None))
    result += if_id(getattr(icon, 'icon_id', None))
    result += if_class(getattr(icon, 'icon_class', None))
    result += if_style(getattr(icon, 'icon_style', None))

    if getattr(icon, 'icon_viewbox', None):
        result += if_key(icon.icon_viewbox, "viewBox")
    if getattr(icon, 'icon_size', None):
        result += f' width="{icon.icon_size}" height="{icon.icon_size}"'
    if getattr(icon, 'icon_fill', None):
        result += if_key(icon.icon_fill, "fill")
    if getattr(icon, 'icon_stroke', None):
        result += if_key(icon.icon_stroke, "stroke")
    if getattr(icon, 'icon_stroke_width', None):
        result += if_key(icon.icon_stroke_width, "stroke-width")

    return result

@typed
def if_input(input: Maybe(_InputBase)=None) -> Str:
    if not input:
        return ""
    result = ""
    result += if_globals(getattr(input, 'globals', None))
    result += if_id(getattr(input, 'input_id', None))
    result += if_class(getattr(input, 'input_class', None))
    result += if_style(getattr(input, 'input_style', None))

    if getattr(input, 'input_type', None):
        result += if_key(input.input_type, "type")
    if getattr(input, 'input_placeholder', None):
        result += if_key(input.input_placeholder, "placeholder")
    if getattr(input, 'input_value', None):
        result += if_key(input.input_value, "value")
    if getattr(input, 'input_name', None):
        result += if_key(input.input_name, "name")
    if getattr(input, 'input_autocomplete', None):
        result += if_key(input.input_autocomplete, "autocomplete")
    if getattr(input, 'input_required', None) and input.input_required:
        result += if_attr("required")
    if getattr(input, 'input_disabled', None) and input.input_disabled:
        result += if_attr("disabled")
    if getattr(input, 'input_readonly', None) and input.input_readonly:
        result += if_attr("readonly")
    if getattr(input, 'input_autofocus', None) and input.input_autofocus:
        result += if_attr("autofocus")
    if getattr(input, 'input_tabindex', None):
        result += if_key(input.input_tabindex, "tabindex")
    if getattr(input, 'input_form_id', None):
        result += if_key(input.input_form_id, "form")
    if getattr(input, 'input_minlength', None):
        result += if_key(input.input_minlength, "minlength")
    if getattr(input, 'input_maxlength', None):
        result += if_key(input.input_maxlength, "maxlength")
    if getattr(input, 'input_pattern', None):
        result += if_key(input.input_pattern, "pattern")
    if getattr(input, 'input_size', None):
        result += if_key(input.input_size, "size")
    if getattr(input, 'input_min', None):
        result += if_key(input.input_min, "min")
    if getattr(input, 'input_max', None):
        result += if_key(input.input_max, "max")
    if getattr(input, 'input_step', None):
        result += if_key(input.input_step, "step")
    if getattr(input, 'input_multiple', None) and input.input_multiple:
        result += if_attr("multiple")
    if getattr(input, 'input_accept', None):
        result += if_key(input.input_accept, "accept")
    if getattr(input, 'input_checked', None) and input.input_checked:
        result += if_attr("checked")
    if getattr(input, 'input_for', None):
        result += if_key(input.input_for, "for")
    return result
