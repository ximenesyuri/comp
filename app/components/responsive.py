from app.mods.decorators.base import component
from app.mods.types.base import Inner
from app.mods.factories.base import Tag
from app.mods.helper.components import (
    _RESPONSIVE,
    _TABLET,
    _DESKTOP,
    _MOBILE,
    _PHONE,
    _NOT_DESKTOP,
    _NOT_PHONE,
    _NOT_MOBILE,
    _NOT_TABLET
)
from app.helper import (
    if_div,
    if_alpine,
)
from app.models import (
    Div,
    Alpine
)

@component
def responsive(div: Div=Div(), alpine: Alpine=_RESPONSIVE, inner: Inner="") -> Tag('div'):
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
def desktop(div: Div=Div(), alpine: Alpine=_DESKTOP, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    return f"""jinja
<div{ div_data }{ alpine_data }>[% if div.div_inner %]
    { div.div_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def tablet(div: Div=Div(), alpine: Alpine=_TABLET, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    return f"""jinja
<div{ div_data }{ alpine_data }>[% if div.div_inner %]
    { div.div_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def phone(div: Div=Div(), alpine: Alpine=_PHONE, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    return f"""jinja
<div{ div_data }{ alpine_data }>[% if div.div_inner %]
    { div.div_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def mobile(div: Div=Div(), alpine: Alpine=_MOBILE, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    return f"""jinja
<div{ div_data }{ alpine_data }>[% if div.div_inner %]
    { div.div_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def not_desktop(div: Div=Div(), alpine: Alpine=_NOT_DESKTOP, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    return f"""jinja
<div{ div_data }{ alpine_data }>[% if div.div_inner %]
    { div.div_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def not_tablet(div: Div=Div(), alpine: Alpine=_NOT_TABLET, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    return f"""jinja
<div{ div_data }{ alpine_data }>[% if div.div_inner %]
    { div.div_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def not_phone(div: Div=Div(), alpine: Alpine=_NOT_PHONE, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    return f"""jinja
<div{ div_data }{ alpine_data }>[% if div.div_inner %]
    { div.div_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def not_mobile(div: Div=Div(), alpine: Alpine=_NOT_MOBILE, inner: Inner="") -> Tag('div'):
    div_data        = if_div(div)
    alpine_data     = if_alpine(alpine)
    return f"""jinja
<div{ div_data }{ alpine_data }>[% if div.div_inner %]
    { div.div_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""
