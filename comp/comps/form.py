from typed import Maybe
from comp.mods.decorators import component
from comp.mods.types.base import Jinja
from comp.models.form import Input
from comp.mods.err import ComponentErr
from comp.mods.helper.comps import if_input

@component
def input(input: Maybe(Input)=None) -> Jinja:
    try:
        if input is None:
            input = Input()
        return f"""jinja
<input{ if_input(input) }>
"""
    except Exception as e:
        raise ComponentErr(e)
