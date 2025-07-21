from typed import typed, Str, Any
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
    Nav
)

@typed
def if_key_value(key: Str="", value: Str="") -> Str:
    if key and value:
        return f' {key}="{value}"'
    return ""

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
def if_globals(globals: Globals=None) -> Str:
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
def if_div(div: Div=None) -> Str:
    if not div:
        return ""
    result = if_globals(getattr(div, 'globals', None))
    result += if_id(getattr(div, 'div_id', None))
    result += if_class(getattr(div, 'div_class', None))
    result += if_style(getattr(div, 'div_style', None))
    return result

@typed
def if_alpine(alpine: Alpine=None) -> Str:
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
def if_text(text: Text=None) -> Str:
    if not text:
        return ""
    result = if_globals(getattr(text, 'globals', None))
    result += if_id(getattr(text, 'text_id', None))
    result += if_class(getattr(text, 'text_class', None))
    result += if_style(getattr(text, 'text_style', None))
    return result

@typed
def if_title(title: Title=None) -> Str:
    if not title:
        return ""
    result = if_globals(getattr(title, 'globals', None))
    result += if_id(getattr(title, 'title_id', None))
    result += if_class(getattr(title, 'title_class', None))
    result += if_style(getattr(title, 'title_style', None))
    return result

@typed
def if_link(link: Link=None) -> Str:
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
def if_button(button: Button=None) -> Str:
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
def if_image(image: Image=None) -> Str:
    if not image:
        return ""
    result = if_globals(getattr(image, 'globals', None))
    result += if_id(getattr(image, 'image_id', None))
    result += if_class(getattr(image, 'image_class', None))
    result += if_style(getattr(image, 'image_style', None))
    if getattr(image, 'image_lazy', None):
        result += if_key_value(image.image_lazy, "loading", "lazy")
    if getattr(image, 'image_alt', None):
        result += if_key(image.image_alt, "alt")
    if getattr(image, 'image_src', None):
        result += if_key(image.image_src, "src")
    return result

@typed
def if_figure(figure: Figure=None) -> Str:
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
def if_asset(asset: Asset=None) -> Str:
    if not asset:
        return ""
    result = ""
    if getattr(asset, 'asset_href', None):
        result += if_key(asset.asset_href, "href")
    if getattr(asset, 'asset_mime', None):
        result += if_key_value(asset.asset_mime, "type", asset.asset_mime)
    if getattr(asset, 'asset_rel', None):
        result += if_key(asset.asset_rel, "rel")
    return result

@typed
def if_item(item: Item=None) -> str:
    if not item:
        return ""
    result = if_id(getattr(item, 'item_id', None))
    result += if_class(getattr(item, 'item_class', None))
    result += if_style(getattr(item, 'item_style', None))
    return result

@typed
def if_ul(ul: Unordered=None) -> str:
    if not ul:
        return ""
    result = if_id(getattr(ul, 'ul_id', None))
    result += if_class(getattr(ul, 'ul_class', None))
    result += if_style(getattr(ul, 'ul_style', None))
    return result

@typed
def if_ol(ol: Ordered=None) -> str:
    if not ol:
        return ""
    result = if_id(getattr(ol, 'ol_id', None))
    result += if_class(getattr(ol, 'ol_class', None))
    result += if_style(getattr(ol, 'ol_style', None))
    return result

@typed
def if_nav(nav: Nav=None) -> str:
    if not nav:
        return ""
    result = if_id(getattr(nav, 'nav_id', None))
    result += if_class(getattr(nav, 'nav_class', None))
    result += if_style(getattr(nav, 'nav_style', None))
    return result
