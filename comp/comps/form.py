from typed import Maybe
from comp.mods.decorators import comp
from comp.mods.types.base import Jinja
from comp.models.form import Input
from comp.mods.err import CompErr
from comp.mods.helper.comps import if_input

@comp
def input(input: Maybe(Input)=None) -> Jinja:
    try:
        if input is None:
            input = Input()
        return f"""jinja
<input{ if_input(input) }>
"""
    except Exception as e:
        raise CompErr(e)
