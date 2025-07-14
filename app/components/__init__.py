from typed import null
from app.mods.decorators.definer import definer
from app.mods.helper.components import (
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

@definer
def div(div: Div=null(Div), alpine: Alpine=null(Alpine), inner: Inner="") -> Tag('div'):
    div_data    = if_div(div)
    alpine_data = if_alpine(alpine)
    return """jinja
<div{{ div_data }}{{ alpine_data }}>
    {{ inner }}
</div>
"""

@definer
def text(text: Text=null(Text), inner: Inner="") -> Tag('p'):
    text_data = if_text(text)
    return """jinja
<p{{ text_data }}>
    {{ inner }}
</p>
"""

@definer
def title(title: Title=null(Title), inner: Inner="") -> Tag('h1','h2','h3','h4','h5','h6'):
    title_data = if_title(title)
    return """jinja
<{{ title.title_tag }}{{ title_data }}>
    {{ inner }}
</{{ title.title_tag }}>
"""

@definer
def link(link: Link=null(Link), inner: Inner="") -> Tag('a'):
    link_data = if_link(link)
    return """jinja
<p{{ link_data }}>
    {{ inner }}
</p>
"""

@definer
def image(image: Image=null(Image)) -> Tag('img'):
    image_data = if_link(image)
    return """jinja
<img{{ image_data }}/>
"""

@definer
def figure(figure: Figure=null(Figure)) -> Tag('figure'):
    figure_data = if_figure(figure)
    image_data = if_image(figure.figure_img)
    return """jinja
<figure{{ figure_data }}>
    <img{{ image_data }}>
    {% if figure.figure_caption %}<figcaption>{{ figure_caption }}</figcaption>{% endif %}
</figure>
"""

@definer
def button(button: Button=null(Button), inner: Inner="") -> Tag('button'):
    button_data = if_button(button)
    return """jinja
<button{{ button_data }}>       
    {{ inner }}
</button>
"""

@definer
def asset(asset: Asset=null(Asset)) -> Tag('link'):
    asset_data = if_asset(asset)
    return """jinja
<link{{ asset_data }}/>
"""

@definer
def script(script: Script=null(Script), inner: Inner="") -> Tag('script'):
    script_data = if_script(script)
    return """jinja
<script{{ script_data }}>
    {{ inner }}
</script>
"""
