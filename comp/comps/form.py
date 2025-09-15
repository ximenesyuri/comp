from comp.mods.decorators import component
from comp.mods.types.base import Jinja
from comp.models.form import Input
from comp.mods.helper.comps import if_input

@component
def input(input: Input=Input()) -> Jinja:
    return f"""jinja
<input{ if_input(input) }>
"""
