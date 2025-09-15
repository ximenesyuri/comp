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
    if_button,
    _render_inner
)

@component
def text(text: Text=Text(), inner: Inner="") -> Jinja:
    if text.text_inner:
        rendered_inner = _render_inner(text.text_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<p{ if_text(text) }>{ rendered_inner }</p>
"""

@component
def title(title: Title=Title(), inner: Inner="") -> Jinja:
    if title.title_inner:
        rendered_inner = _render_inner(title.title_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<{ title.title_tag }{ if_title(title) }>{ rendered_inner }</{ title.title_tag }>
"""

@component
def link(link: Link=Link(), inner: Inner="") -> Jinja:
    if link.link_inner:
        rendered_inner = _render_inner(link.link_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<a{ if_link(link) }>{ rendered_inner }</a>
"""

@component
def img(img: Img=Img()) -> Tag('img'):
    return f"""jinja
<img{ if_img(img) }/>
"""

@component
def figure(figure: Figure=Figure()) -> Tag('figure'):
    return f"""jinja
<figure{ if_figure(figure) }>
    <img{ if_img(figure.figure_img) }>
    [% if figure.figure_caption is defined %]<figcaption>{ figure.figure_caption }</figcaption>[% endif %]
</figure>
"""

@component
def button(button: Button=Button(), inner: Inner="") -> Jinja:
    if button.button_inner:
        rendered_inner = _render_inner(button.button_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<button{ if_button(button) }>{ rendered_inner }</button>
"""

@component
def logo(logo: Logo=Logo()) -> Jinja:
    return f"""jinja
<a{ if_img(logo.logo_img) }><img{ if_link(logo.logo_link) }></a>
"""
