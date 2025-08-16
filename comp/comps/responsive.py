from comp.mods.decorators import component
from comp.mods.types.base import Inner
from comp.mods.types.factories import Tag

@component
def desktop(inner: Inner="") -> Tag('div'):
    div_class="desktop"
    return f"""jinja
<div class="{ div_class }">[% if inner %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def tablet(inner: Inner="") -> Tag('div'):
    div_class="tablet"
    return f"""jinja
<div class="{ div_class }">[% if inner %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def phone(inner: Inner="") -> Tag('div'):
    div_class="phone"
    return f"""jinja
<div class="{ div_class }">[% if inner %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def mobile(inner: Inner="") -> Tag('div'):
    div_class="mobile"
    return f"""jinja
<div class="{ div_class }">[% if inner %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def not_desktop(inner: Inner="") -> Tag('div'):
    div_class="not:desktop"
    return f"""jinja
<div class="{ div_class }">[% if inner %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def not_tablet(inner: Inner="") -> Tag('div'):
    div_class="not:tablet"
    return f"""jinja
<div class="{ div_class }">[% if inner %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def not_phone(inner: Inner="") -> Tag('div'):
    div_class="not:phone"
    return f"""jinja
<div class="{ div_class }">[% if inner %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def not_mobile(inner: Inner="") -> Tag('div'):
    div_class="not:mobile"
    return f"""jinja
<div class="{ div_class }">[% if inner %]
    { inner }
</div>[% else %]</div>[% endif %]
"""
