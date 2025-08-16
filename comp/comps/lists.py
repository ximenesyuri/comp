from comp.mods.decorators import component
from comp.mods.types.base import Jinja, Inner
from comp.models.lists import Item, Unordered, Ordered, Nav
from comp.comps.content import link
from comp.mods.helper.comps import (
    if_item,
    if_ul,
    if_ol,
    if_nav,
    if_id,
    if_class,
    if_style
)

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
