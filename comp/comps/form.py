from comp.mods.decorators import component
from comp.mods.types.base import Jinja
from comp.models.form import Input
from comp.mods.helper.comps import if_input

@component
def input(input: Input=Input()) -> Jinja:
    input_data = if_input(input)
    return f"""jinja
<input{input_data}>
"""
