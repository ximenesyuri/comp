from typed import null
from app.mods.types.base import Inner, Jinja
from app.mods.factories.base import Tag
from app.mods.decorators.base import component
from app.helper import (
    if_key,
    if_id,
    if_class,
    if_header,
    if_aside,
    if_sidebar,
    if_div,
    if_style,
    if_alpine,
    if_text,
    if_title,
    if_button,
    if_link,
    if_text,
    if_img,
    if_figure,
    if_script,
    if_asset,
    if_item,
    if_ul,
    if_ol,
    if_nav,
    if_input
)
from app.models import (
    Header,
    Aside,
    Sidebar,
    Div,
    Alpine,
    Button,
    Title,
    Text,
    Image,
    Link,
    Figure,
    Script,
    Asset,
    Item,
    Ordered,
    Unordered,
    Nav,
    Logo,
    Input
)


@component
def header(header: Header=Header(), inner: Inner="") -> Jinja:
    return f"""jinja
<div{ if_header(header) }>[% if header.header_inner %]
    { header.header_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def aside(aside: Aside=Aside(), inner: Inner="") -> Jinja:
    return f"""jinja
<div{ if_aside(aside) }>[% if aside.aside_inner %]
    { aside.aside_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def div(div: Div=Div(), alpine: Alpine=Alpine(), inner: Inner="") -> Jinja:
    div_data    = if_div(div)
    alpine_data = if_alpine(alpine)
    return f"""jinja
<div{ div_data }{ alpine_data }>[% if div.div_inner %]
    { div.div_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def alpine(alpine: Alpine=Alpine(), inner: Inner="") -> Jinja:
    alpine_data = if_alpine(alpine)
    return f"""jinja
<div{ alpine_data }>[% if inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def text(text: Text=Text(), inner: Inner="") -> Jinja:
    text_data = if_text(text)
    return f"""jinja
<p{ text_data }>[% if text.text_inner %]
    { text.text_inner }
</p>[% elif inner is defined %]
    { inner }
</p>[% else %]</p>[% endif %]
"""

@component
def title(title: Title=Title(), inner: Inner="") -> Jinja:
    title_data = if_title(title)
    return f"""jinja
<{ title.title_tag }{ title_data }>[% if title.title_inner %]
    { title.title_inner }
</{ title.title_tag }>[% elif inner is defined %]
    { inner }
</{ title.title_tag }>[% else %]</{ title.title_tag }>[% endif %]
"""

@component
def link(link: Link=Link(), inner: Inner="") -> Jinja:
    link_data = if_link(link)
    return f"""jinja
<a{ link_data }>[% if link.link_inner %]
    { link.link_inner }
</a>[% elif inner is defined %]
    { inner }
</a>[% else %]</a>[% endif %] 
"""

@component
def img(img: Image=Image()) -> Tag('img'):
    return f"""jinja
<img{ if_img(img) }/>
"""

@component
def figure(figure: Figure=Figure()) -> Tag('figure'):
    figure_data = if_figure(figure)
    img_data = if_img(figure.figure_img)
    return f"""jinja
<figure{ figure_data }>
    <img{ img_data }>
    [% if figure.figure_caption %]<figcaption>{ figure_caption }</figcaption>[% endif %]
</figure>
"""

@component
def button(button: Button=Button(), inner: Inner="") -> Jinja:
    button_data = if_button(button)
    return f"""jinja 
<button{ button_data }>[% if button.button_inner %]
    { button.button_inner }
</button>[% elif inner is defined %]
    { inner }
</button>[% else %]</button>[% endif %]
"""

@component
def asset(asset: Asset=Asset()) -> Tag('link'):
    return f"""jinja
<link{ if_asset(asset) }/>
"""

@component
def script(script: Script=Script(), inner: Inner="") -> Jinja:
    script_data = if_script(script)
    return f"""jinja
<script{ script_data }>[% if script.script_inner %]
    { script.script_inner }
</script>[% elif inner is defined %]
    { inner }
</script>[% else %]</script>[% endif %]
"""

@component
def item(item: Item=Item(), inner: Inner="") -> Jinja:
    item_data = if_item(item)
    return f"""jinja
<li{ item_data }>[% if item.item_inner %]
    { item.item_inner }
</li>[% elif inner is defined %]
    { inner }
</li>[% else %]</li>[% endif %]
"""
li = item

@component
def unordered(ul: Unordered=Unordered(), __context__={"item": item}) -> Jinja:
    ul_data = if_ul(ul)
    return f"""jinja
<ul{ ul_data }>[% if ul.ul_items %][% for i in ul.ul_items %]
    [[ item(item=i) ]][% endfor %]
</ul>[% else %]</ul>[% endif %]
"""
ul = unordered

@component
def ordered(ol: Ordered=Ordered(), __context__={"item": item}) -> Jinja:
    ol_data = if_ol(ol)
    return f"""jinja
<ol{ ol_data }>[% if ol.ol_items %][% for i in ol.ol_items %]
    [[ item(item=i) ]][% endfor %]
</ol>[% else %]</ol>[% endif %]
"""
ol = ordered


@component
def nav(nav: Nav=Nav(), __context__={"link": link, "item": item}) -> Jinja:
    nav_data = if_nav(nav)
    ul_id = if_id(nav.ul_id)
    ul_class = if_class(nav.ul_class)
    ul_style = if_style(nav.ul_style)
    if nav.nav_direction == "horizontal":
        ul_style = f" style='display: flex; flex-direction: row; {nav.ul_style}'"
    else:
        ul_style = f" style='display: flex; flex-direction: column; {nav.ul_style}'"

    return f"""jinja
<nav{ nav_data }>[% if nav.nav_items %]
    <ul{ ul_id }{ ul_class }{ ul_style }>[% for it in nav.nav_items %]
        [[ item(item=it, inner=link(link=it.item_link)) ]][% endfor %]
    </ul>
</nav>[% else %]</nav>[% endif %]
"""

@component
def logo(logo: Logo=Logo()) -> Jinja:
    img_data = if_img(logo.logo_img)
    link_data = if_link(logo.logo_link)
    return f"""jinja
<a{link_data}><img{img_data}></a>
"""

@component
def input(input: Input=Input()) -> Jinja:
    input_data = if_input(input)
    return f"""jinja
<input{input_data}>
"""
