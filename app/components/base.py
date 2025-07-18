from typed import null
from app.mods.types.base import Inner, Jinja
from app.mods.factories.base import Tag
from app.mods.decorators.base import component
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
def div(div: Div=Div(), alpine: Alpine=Alpine(), inner: Inner="") -> Jinja:
    div_data    = if_div(div)
    alpine_data = if_alpine(alpine)
    return """jinja
<div{{ div_data }}{{ alpine_data }}>{% if inner is defined %}
    {{ inner }}
</div>{% else %}</div>{% endif %}
"""

@component
def text(text: Text=Text(), inner: Inner="") -> Jinja:
    text_data = if_text(text)
    return """jinja
<p{{ text_data }}>{% if inner %}
    {{ inner }}
</p>{% else %}</p>{% endif %}
"""

@component
def title(title: Title=Title(), inner: Inner="") -> Jinja:
    title_data = if_title(title)
    return """jinja
<{{ title.title_tag }}{{ title_data }}>{% if inner %}
    {{ inner }}
</{{ title.title_tag }}>{% else %}</{{ title.title_tag }}>{% endif %}
"""

@component
def link(link: Link=Link(), inner: Inner="") -> Jinja:
    link_data = if_link(link)
    return """jinja
<a{{ link_data }}>{% if inner %}
    {{ inner }}
</a>{% else %}</a>{% endif %} 
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
def button(button: Button=Button(), inner: Inner="") -> Jinja:
    button_data = if_button(button)
    return """jinja
<button{{ button_data }}>{% if inner %}
    {{ inner }}
</button>{% else %}</button>{% endif %}
"""

@component
def asset(asset: Asset=Asset()) -> Tag('link'):
    asset_data = if_asset(asset)
    return """jinja
<link{{ asset_data }}/>
"""

@component
def script(script: Script=Script(), inner: Inner="") -> Jinja:
    script_data = if_script(script)
    return """jinja
<script{{ script_data }}>{% if inner %}
    {{ inner }}
</script>{% else %}</script>{% endif %}
"""
