from typed import null
from comp.mods.types.base import Inner, Jinja
from comp.mods.types.factories import Tag
from comp.mods.decorators import component
from comp.mods.helper.components import if_script, if_asset
from comp.models import Script, Asset


@component
def asset(asset: Asset=Asset()) -> Tag('link'):
    return f"""jinja
<link{ if_asset(asset) }/>
"""

@component
def script(script: Script=Script(), inner: Inner="") -> Jinja:
    script_data = if_script(script)
    return f"""jinja
<script{ script_data }>[% if script.script_inner %]
    { script.script_inner }
</script>[% elif inner is defined %]
    { inner }
</script>[% else %]</script>[% endif %]
"""
