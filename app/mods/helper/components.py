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
    Asset
)

@typed
def if_key_value(entry: Any=None, key: Str="", value: Str="") -> Maybe(Str):
    if entry and key and value:
        f"{{% if {entry} %}} {key}=\"{{{{{value}}}}}\"{{% endif %}}"

@typed
def if_key(entry: Any=None, what: Str="id") -> Maybe(Str):
    if entry and what:
        f"{{% if {entry} %}} {what}=\"{{{{{entry}}}}}\"{{% endif %}}"

@typed
def if_attr(entry: Any=None, attr: Str="id") -> Maybe(Str):
    if entry and attr:
        f"{{% if {entry} %}} {attr}{{% endif %}}"


@typed
def if_globals(globals: Globals={}) -> Maybe(Str):
    return f'{if_key(globals.title, "title")}{if_key(globals.tabindex, "tabindex")}{if_key(globals.accesskey, "")}{if_key(globals.anchor, "anchor")}{if_attr(globals.hidden, "hidden")}'

@typed
def if_id(entry: Any=None) -> Maybe(Str):
    return if_key(entry, "id")

@typed
def if_class(entry: Any=None) -> Maybe(Str):
    return if_key(entry, 'class')

@typed
def if_hover(entry: Any=None) -> Maybe(Str):
    return if_key(entry, "hover")

@typed
def if_div(div: Div={}) -> Maybe(Str):
    if div:
        return f"{if_globals(div.globals)}{if_id(div.div_id)}{if_class(div.div_class)}{if_hover(div.div_hover)}"

@typed
def if_alpine(alpine: Alpine={}) -> Maybe(Str):
    if div:
        return f'{if_key(alpine.x_init, "x-init")}{if_key(alpine.x_show, "x-show")}{if_key(alpine.x_data, "x-data")}{if_attr(alpine.x_cloak, "x-cloak")}'

@typed
def if_text(text: Text={}) -> Maybe(Str):
    if text:
        return f"{if_globals(text.globals)}{if_id(text.text_id)}{if_class(text.text_class)}{if_hover(text.text_hover)}"

@typed
def if_title(title: Title={}) -> Maybe(Str):
    if title:
        return f"{if_globals(title.globals)}{if_id(title.title_id)}{if_class(title.title_class)}{if_hover(title.title_hover)}"

@typed
def if_link(link: Link={}) -> Maybe(Str):
    if link:
        return f'{if_globals(link.globals)}{if_id(link.link_id)}{if_class(link.link_class)}{if_hover(link.link_hover)}{if_key(link.link_href), "href"}{if_key(link.link_download), "download"}{if_key(link.link_rel), "rel"}{if_key(link.link_target), "target"}'

@typed
def if_button(button: Button=None) -> Maybe(Str):
    if button:
        return f"{if_globals(button.globals)}{if_id(button.button_id)}{if_class(button.button_class)}{if_hover(button.button_hover)}{if_key(button.on_click, "@on_click")}{if_key(button.click_away, "@click_away")}"

@typed
def if_image(image: Image={}) -> Maybe(Str):
    if image:
        return f'{if_globals(image.globals)}{if_id(image.image_id)}{if_class(image.image_class)}{if_hover(image.image_hover)}{if_key_value(image.image_lazy, "loading", "lazy")}{if_key(image.image_alt, "alt")}{if_key(image.image_src, "src")}'

@typed
def if_figure(figure: Figure={}) -> Maybe(Str):
    if figure:
        return f'{if_globals(figure.globals)}'

@typed
def if_script(script: Script={}) -> Maybe(Str):
    if script:
        return f'{if_key(script.script_src)}{if_key(script.script_type)}{if_attr(script.script_defer)}{if_attr(script.script_async)}'

@typed
def if_asset(asset: Asset={}) -> Maybe(Str):
    if asset:
        return f'{if_key(asset.asset_href)}{if_key_value(asset.asset_mime, "type", asset.asset_mime)}{if_key(asset.asset_rel, "rel")}'
