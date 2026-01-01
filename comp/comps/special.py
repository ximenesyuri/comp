from typed import Maybe
from comp.mods.decorators import component
from comp.mods.types.base import Content, Jinja
from comp.models.special import Markdown
from comp.mods.err import ComponentErr

@component
def content(content: Content='') -> Jinja:
    try:
        return f"""jinja
{ content }        
 """
    except Exception as e:
        raise ComponentErr(e)

@component
def markdown(markdown: Maybe(Markdown)=None) -> Jinja:
    try:
        if markdown is None:
            markdown = Markdown()
        return f"""jinja
{ markdown.content }        
"""
    except Exception as e:
        raise ComponentErr(e)
