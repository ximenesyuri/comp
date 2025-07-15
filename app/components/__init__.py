from typed import null
from app.mods.types.base import Inner
from app.mods.factories.base import Tag
from app.mods.decorators.component import component
from app.mods.helper.components import (
    _X_DATA_RESPONSIVE,
    _RESPONSIVE,
    _TABLET,
    _DESKTOP,
    _MOBILE,
    _PHONE,
    _NOT_DESKTOP,
    _NOT_PHONE,
    _NOT_MOBILE,
    _NOT_TABLET
)
from app.helper import (
    if_key,
    if_div,
    if_alpine,
    if_text,
    if_title,
    if_button,
    if_link,
    if_text,
    if_image,
    if_figure,
    if_script,
    if_asset
)
from app.models import (
    Div,
    Alpine,
    Button,
    Title,
    Text,
    Image,
    Link,
    Figure,
    Script,
    Asset
)

@component
def div(div: Div=Div(), alpine: Alpine=Alpine(), inner: Inner="") -> Tag('div'):
    div_data    = if_div(div)
    alpine_data = if_alpine(alpine)
    return """jinja
<div{{ div_data }}{{ alpine_data }}>
    {{ inner }}
</div>
"""

@component
def text(text: Text=Text(), inner: Inner="") -> Tag('p'):
    text_data = if_text(text)
    return """jinja
<p{{ text_data }}>
    {{ inner }}
</p>
"""

@component
def title(title: Title=Title(), inner: Inner="") -> Tag('h1','h2','h3','h4','h5','h6'):
    title_data = if_title(title)
    return """jinja
<{{ title.title_tag }}{{ title_data }}>
    {{ inner }}
</{{ title.title_tag }}>
"""

@component
def link(link: Link=Link(), inner: Inner="") -> Tag('a'):
    link_data = if_link(link)
    return """jinja
<a{{ link_data }}>
    {{ inner }}
</a>
"""

@component
def image(image: Image=Image()) -> Tag('img'):
    image_data = if_link(image)
    return """jinja
<img{{ image_data }}/>
"""

@component
def figure(figure: Figure=Figure()) -> Tag('figure'):
    figure_data = if_figure(figure)
    image_data = if_image(figure.figure_img)
    return """jinja
<figure{{ figure_data }}>
    <img{{ image_data }}>
    {% if figure.figure_caption %}<figcaption>{{ figure_caption }}</figcaption>{% endif %}
</figure>
"""

@component
def button(button: Button=Button(), inner: Inner="") -> Tag('button'):
    button_data = if_button(button)
    return """jinja
<button{{ button_data }}>       
    {{ inner }}
</button>
"""

@component
def asset(asset: Asset=Asset()) -> Tag('link'):
    asset_data = if_asset(asset)
    return """jinja
<link{{ asset_data }}/>
"""

@component
def script(script: Script=Script(), inner: Inner="") -> Tag('script'):
    script_data = if_script(script)
    return """jinja
<script{{ script_data }}>
    {{ inner }}
</script>
"""

@component
def responsive(div: Div=Div(), alpine: Alpine=_RESPONSIVE, inner: Inner="") -> Tag('div'):
    div_data    = if_div(div)
    alpine_data = if_alpine(alpine)
    return """jinja
<div{{ div_data }}{{ alpine_data }}>
    {{ inner }}
</div>
"""

@component
def desktop(div: Div=Div(), alpine: Alpine=_DESKTOP, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    responsive_data = _X_DATA_RESPONSIVE
    return """jinja
<div x-data="{{ responsive_data }}">
    <div{{ div_data }}{{ alpine_data }}>
        {{ inner }}
    </div>
</div>
"""

@component
def tablet(div: Div=Div(), alpine: Alpine=_TABLET, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    responsive_data = _X_DATA_RESPONSIVE
    return """jinja
<div x-data="{{ responsive_data }}">
    <div{{ div_data }}{{ alpine_data }}>
        {{ inner }}
    </div>
</div>
"""

@component
def phone(div: Div=Div(), alpine: Alpine=_PHONE, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    responsive_data = _X_DATA_RESPONSIVE
    return """jinja
<div x-data="{{ responsive_data }}">
    <div{{ div_data }}{{ alpine_data }}>
        {{ inner }}
    </div>
</div>
"""

@component
def mobile(div: Div=Div(), alpine: Alpine=_MOBILE, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    responsive_data = _X_DATA_RESPONSIVE
    return """jinja
<div x-data="{{ responsive_data }}">
    <div{{ div_data }}{{ alpine_data }}>
        {{ inner }}
    </div>
</div>
"""

@component
def not_desktop(div: Div=Div(), alpine: Alpine=_NOT_DESKTOP, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    responsive_data = _X_DATA_RESPONSIVE
    return """jinja
<div x-data="{{ responsive_data }}">
    <div{{ div_data }}{{ alpine_data }}>
        {{ inner }}
    </div>
</div>
"""

@component
def not_tablet(div: Div=Div(), alpine: Alpine=_NOT_TABLET, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    responsive_data = _X_DATA_RESPONSIVE
    return """jinja
<div x-data="{{ responsive_data }}">
    <div{{ div_data }}{{ alpine_data }}>
        {{ inner }}
    </div>
</div>
"""

@component
def not_phone(div: Div=Div(), alpine: Alpine=_NOT_PHONE, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    responsive_data = _X_DATA_RESPONSIVE
    return """jinja
<div x-data="{{ responsive_data }}">
    <div{{ div_data }}{{ alpine_data }}>
        {{ inner }}
    </div>
</div>
"""

@component
def not_mobile(div: Div=Div(), alpine: Alpine=_NOT_MOBILE, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    responsive_data = _X_DATA_RESPONSIVE
    return """jinja
<div x-data="{{ responsive_data }}">
    <div{{ div_data }}{{ alpine_data }}>
        {{ inner }}
    </div>
</div>
"""
