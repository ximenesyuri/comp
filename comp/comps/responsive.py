from comp.mods.decorators import component
from comp.mods.types.base import Inner
from comp.mods.types.factories import Tag
from comp.mods.helper.comps import _render_inner
from comp.mods.err import ComponentErr

@component
def desktop(inner: Inner="") -> Tag('div'):
    try:
        div_class="desktop"
        if inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""

        return f"""jinja
<div class="{ div_class }">{ rendered_inner }</div>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def tablet(inner: Inner="") -> Tag('div'):
    try:
        div_class="tablet"
        if inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""

        return f"""jinja
<div class="{ div_class }">{ rendered_inner }</div>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def phone(inner: Inner="") -> Tag('div'):
    try:
        div_class="phone"
        if inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""

        return f"""jinja
<div class="{ div_class }">{ rendered_inner }</div>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def mobile(inner: Inner="") -> Tag('div'):
    try:
        div_class="mobile"
        if inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""

        return f"""jinja
<div class="{ div_class }">{ rendered_inner }</div>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def not_desktop(inner: Inner="") -> Tag('div'):
    try:
        div_class="not:desktop"
        if inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""

        return f"""jinja
<div class="{ div_class }">{ rendered_inner }</div>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def not_tablet(inner: Inner="") -> Tag('div'):
    try:
        div_class="not:tablet"
        if inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""

        return f"""jinja
<div class="{ div_class }">{ rendered_inner }</div>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def not_phone(inner: Inner="") -> Tag('div'):
    try:
        div_class="not:phone"
        if inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""

        return f"""jinja
<div class="{ div_class }">{ rendered_inner }</div>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def not_mobile(inner: Inner="") -> Tag('div'):
    try:
        div_class="not:mobile"
        if inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""

        return f"""jinja
<div class="{ div_class }">{ rendered_inner }</div>
"""
    except Exception as e:
        raise ComponentErr(e)
