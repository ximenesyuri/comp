from app.mods.decorators.base import component
from app.mods.types.base import Inner
from app.mods.factories.base import Tag
from app.helper import (
    if_div,
    if_alpine,
)
from app.models import (
    Div,
    Alpine
)

@component
def desktop(div: Div=Div(), inner: Inner="") -> Tag('desktop'):
    div_data = if_div(div)
    return f"""jinja
<desktop{ div_data }>[% if div.div_inner %]
    { div.div_inner }
</desktop>[% elif inner is defined %]
    { inner }
</desktop>[% else %]</desktop>[% endif %]
"""

@component
def tablet(div: Div=Div(), inner: Inner="") -> Tag('tablet'):
    div_data = if_div(div)
    return f"""jinja
<tablet{ div_data }>[% if div.div_inner %]
    { div.div_inner }
</tablet>[% elif inner is defined %]
    { inner }
</tablet>[% else %]</tablet>[% endif %]
"""

@component
def phone(div: Div=Div(), inner: Inner="") -> Tag('phone'):
    div_data = if_div(div)
    return f"""jinja
<phone{ div_data }>[% if div.div_inner %]
    { div.div_inner }
</phone>[% elif inner is defined %]
    { inner }
</phone>[% else %]</phone>[% endif %]
"""

@component
def mobile(div: Div=Div(), inner: Inner="") -> Tag('mobile'):
    div_data = if_div(div)
    return f"""jinja
<mobile{ div_data }>[% if div.div_inner %]
    { div.div_inner }
</mobile>[% elif inner is defined %]
    { inner }
</mobile>[% else %]</mobile>[% endif %]
"""

@component
def not_desktop(div: Div=Div(), inner: Inner="") -> Tag('not-desktop'):
    div_data = if_div(div)
    return f"""jinja
<not-desktop{ div_data }>[% if div.div_inner %]
    { div.div_inner }
</not-desktop>[% elif inner is defined %]
    { inner }
</not-desktop>[% else %]</not-desktop>[% endif %]
"""

@component
def not_tablet(div: Div=Div(), inner: Inner="") -> Tag('not-tablet'):
    div_data = if_div(div)
    return f"""jinja
<not-tablet{ div_data }>[% if div.div_inner %]
    { div.div_inner }
</not-tablet>[% elif inner is defined %]
    { inner }
</not-tablet>[% else %]</not-tablet>[% endif %]
"""

@component
def not_phone(div: Div=Div(), inner: Inner="") -> Tag('not-phone'):
    div_data = if_div(div)
    return f"""jinja
<not-phone{ div_data }>[% if div.div_inner %]
    { div.div_inner }
</not-phone>[% elif inner is defined %]
    { inner }
</not-phone>[% else %]</not-phone>[% endif %]
"""

@component
def not_mobile(div: Div=Div(), inner: Inner="") -> Tag('not-mobile'):
    div_data = if_div(div)
    return f"""jinja
<not-mobile{ div_data }>[% if div.div_inner %]
    { div.div_inner }
</not-mobile>[% elif inner is defined %]
    { inner }
</not-mobile>[% else %]</not-mobile>[% endif %]
"""
