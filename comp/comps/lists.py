from typed import Maybe
from comp.mods.decorators import comp
from comp.mods.types.base import Jinja, Inner
from comp.mods.err import CompErr
from comp.models.lists import Item, Unordered, Ordered, Nav
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

@comp
def item(item: Maybe(Item)=None, inner: Inner="") -> Jinja:
    try:
        if item is None:
            item = Item()
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
        raise CompErr(e)
li = item

@comp
def unordered(ul: Maybe(Unordered)=None, __context__={"item": item}) -> Jinja:
    try:
        if ul is None:
            ul = Unordered()
        return f"""jinja
<ul{ if_ul(ul) }>[% if ul.ul_items is defined %][% for i in ul.ul_items %]
    [[ item(item=i) ]][% endfor %]
</ul>[% else %]</ul>[% endif %]
"""
    except Exception as e:
        raise CompErr(e)
ul = unordered

@comp
def ordered(ol: Maybe(Ordered)=None, __context__={"item": item}) -> Jinja:
    try:
        if ol is None:
            ol = Ordered()
        return f"""jinja
<ol{ if_ol(ol) }>[% if ol.ol_items is defined %][% for i in ol.ol_items %]
    [[ item(item=i) ]][% endfor %]
</ol>[% else %]</ol>[% endif %]
"""
    except Exception as e:
        raise CompErr(e)
ol = ordered

@comp
def nav(nav: Maybe(Nav)=None, __context__={"link": link, "item": item}) -> Jinja:
    try:
        if nav is None:
            nav = Nav()
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
        raise CompErr(e)
