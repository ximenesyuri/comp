from typed import Maybe
from comp.mods.types.base import Inner, Jinja
from comp.mods.types.factories import Tag
from comp.mods.decorators import comp
from comp.models.content import Text, Title, Link, Img, Figure, Button, Logo
from comp.mods.err import CompErr
from comp.mods.helper.comps import (
    if_text,
    if_title,
    if_link,
    if_img,
    if_figure,
    if_button,
    _render_inner
)

@comp
def text(text: Maybe(Text)=None, inner: Inner="") -> Jinja:
    try:
        if text is None:
            text = Text()
        if text.text_inner:
            rendered_inner = _render_inner(text.text_inner)
        elif inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""
        return f"""jinja
<p{ if_text(text) }>{ rendered_inner }</p>
"""
    except Exception as e:
        raise CompErr(e)

@comp
def title(title: Maybe(Title)=None, inner: Inner="") -> Jinja:
    try:
        if title is None:
            title = Title()
        if title.title_inner:
            rendered_inner = _render_inner(title.title_inner)
        elif inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""
        return f"""jinja
<{ title.title_tag }{ if_title(title) }>{ rendered_inner }</{ title.title_tag }>
"""
    except Exception as e:
        raise CompErr(e)

@comp
def link(link: Maybe(Link)=None, inner: Inner="") -> Jinja:
    try:
        if link is None:
            link = Link()
        if link.link_inner:
            rendered_inner = _render_inner(link.link_inner)
        elif inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""
        return f"""jinja
<a{ if_link(link) }>{ rendered_inner }</a>
"""
    except Exception as e:
        raise CompErr(e)

@comp
def image(img: Maybe(Img)=None) -> Tag('img'):
    try:
        if img is None:
            img = Img()
        return f"""jinja
<img{ if_img(img) }/>
"""
    except Exception as e:
        raise CompErr(e)
img = image

@comp
def figure(figure: Maybe(Figure)=None) -> Tag('figure'):
    try:
        if figure is None:
            figure = Figure()
        return f"""jinja
<figure{ if_figure(figure) }>
    <img{ if_img(figure.figure_img) }>
    [% if figure.figure_caption is defined %]<figcaption>{ figure.figure_caption }</figcaption>[% endif %]
</figure>
"""
    except Exception as e:
        raise CompErr(e)
fig = figure

@comp
def button(button: Maybe(Button)=None, inner: Inner="") -> Jinja:
    try:
        if button is None:
            button = Button()
        if button.button_inner:
            rendered_inner = _render_inner(button.button_inner)
        elif inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""
        return f"""jinja
<button{ if_button(button) }>{ rendered_inner }</button>
"""
    except Exception as e:
        raise CompErr(e)

@comp
def logo(logo: Maybe(Logo)=None) -> Jinja:
    try:
        if logo is None:
            logo = Logo()
        return f"""jinja
<a{ if_img(logo.logo_img) }><img{ if_link(logo.logo_link) }></a>
"""
    except Exception as e:
        raise CompErr(e)
