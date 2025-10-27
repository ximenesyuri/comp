from comp.mods.decorators import component
from comp.mods.types.base import Content, Jinja
from comp.mods.err import ComponentErr

@component
def content(content: Content='') -> Jinja:
    try:
        return f"""jinja
{ content }        
 """
    except Exception as e:
        raise ComponentErr(e)
