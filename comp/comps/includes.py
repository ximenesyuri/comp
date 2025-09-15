from typed import null
from comp.mods.types.base import Inner, Jinja
from comp.mods.types.factories import Tag
from comp.mods.decorators import component
from comp.models import Script, Asset
from comp.mods.helper.comps import (
    if_script,
    if_asset,
    _render_inner
)


@component
def asset(asset: Asset=Asset()) -> Tag('link'):
    return f"""jinja
<link{ if_asset(asset) }/>
"""

@component
def script(script: Script=Script(), inner: Inner="") -> Jinja:
    if script.script_inner:
        rendered_inner = _render_inner(script.script_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<script{ if_script(script) }>{ rendered_inner }</script>
"""
