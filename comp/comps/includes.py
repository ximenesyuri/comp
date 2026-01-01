from typed import Maybe
from comp.mods.types.base import Inner, Jinja
from comp.mods.types.factories import Tag
from comp.mods.decorators import comp
from comp.mods.err import CompErr
from comp.models import Script, Asset
from comp.mods.helper.comps import (
    if_script,
    if_asset,
    _render_inner
)


@comp
def asset(asset: Maybe(Asset)=None) -> Tag('link'):
    try:
        if asset is None:
            asset = Asset()
        return f"""jinja
<link{ if_asset(asset) }/>
"""
    except Exception as e:
        raise CompErr(e)

@comp
def script(script: Maybe(Script)=None, inner: Inner="") -> Jinja:
    try:
        if script is None:
            script = Script()

        if script.script_inner:
            rendered_inner = _render_inner(script.script_inner)
        elif inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""
        return f"""jinja
<script{ if_script(script) }>{ rendered_inner }</script>
"""
    except Exception as e:
        raise CompErr(e)
