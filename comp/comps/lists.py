from comp.mods.decorators import component
from comp.mods.types.base import Jinja, Inner
from comp.mods.err import ComponentErr
from comp.models.lists import Item, Unordered, Ordered, NavItem, Nav
from comp.comps.content import link
from comp.mods.helper.comps import (
    if_item,
    if_ul,
    if_ol,
    if_nav,
    if_id,
    if_class,
    if_style,
    _render_inner
)

@component
def item(item: Item=Item(), inner: Inner="") -> Jinja:
    try:
        if item.item_inner:
            rendered_inner = _render_inner(item.item_inner)
        elif inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""
        return f"""jinja
<li{ if_item(item) }>{ rendered_inner }</li>
"""
    except Exception as e:
        raise ComponentErr(e)
li = item

@component
def unordered(ul: Unordered=Unordered(), __context__={"item": item}) -> Jinja:
    try:
        return f"""jinja
<ul{ if_ul(ul) }>[% if ul.ul_items is defined %][% for i in ul.ul_items %]
    [[ item(item=i) ]][% endfor %]
</ul>[% else %]</ul>[% endif %]
"""
    except Exception as e:
        raise ComponentErr(e)
ul = unordered

@component
def ordered(ol: Ordered=Ordered(), __context__={"item": item}) -> Jinja:
    try:
        return f"""jinja
<ol{ if_ol(ol) }>[% if ol.ol_items is defined %][% for i in ol.ol_items %]
    [[ item(item=i) ]][% endfor %]
</ol>[% else %]</ol>[% endif %]
"""
    except Exception as e:
        raise ComponentErr(e)
ol = ordered

@component
def nav(nav: Nav=Nav(), __context__={"link": link, "item": item}) -> Jinja:
    try:
        ul_style = if_style(nav.ul_style)
        if nav.nav_direction == "horizontal":
            ul_style = f" style='display: flex; flex-direction: row; {nav.ul_style}'"
        else:
            ul_style = f" style='display: flex; flex-direction: column; {nav.ul_style}'"

        return f"""jinja
<nav{ if_nav(nav) }>[% if nav.nav_items is defined %]
    <ul{ if_id(nav.ul_id) }{ if_class(nav.ul_class) }{ ul_style }>[% for it in nav.nav_items %]
        [[ item(item=it, inner=link(link=it.item_link)) ]][% endfor %]
    </ul>
</nav>[% else %]</nav>[% endif %]
"""
    except Exception as e:
        raise ComponentErr(e)
