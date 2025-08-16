from comp.mods.types.base import Inner, Jinja
from comp.mods.types.factories import Tag
from comp.mods.decorators import component
from comp.models.content import Text, Title, Link, Img, Figure, Button, Logo
from comp.mods.helper.comps import (
    if_text,
    if_title,
    if_link,
    if_img,
    if_figure,
    if_button
)

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
def img(img: Img=Img()) -> Tag('img'):
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
def logo(logo: Logo=Logo()) -> Jinja:
    img_data = if_img(logo.logo_img)
    link_data = if_link(logo.logo_link)
    return f"""jinja
<a{link_data}><img{img_data}></a>
"""
