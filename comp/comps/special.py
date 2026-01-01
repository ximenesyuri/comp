from typed import Maybe
from comp.mods.decorators import comp
from comp.mods.types.base import Content, Jinja
from comp.models.special import Markdown
from comp.mods.err import CompErr

@comp
def content(content: Content='') -> Jinja:
    try:
        return f"""jinja
{ content }        
 """
    except Exception as e:
        raise CompErr(e)

@comp
def markdown(markdown: Maybe(Markdown)=None) -> Jinja:
    try:
        if markdown is None:
            markdown = Markdown()
        return f"""jinja
{ markdown.content }        
"""
    except Exception as e:
        raise CompErr(e)
