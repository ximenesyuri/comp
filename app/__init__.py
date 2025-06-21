from typed import Str, List, TypedFunc, Any
from app.main import *

import re

@component
def my_tag_component(aa: Str) -> TagStr('header'):
    return """jinja
        <header> 
            {{aa}}
        </header>
    """

tag_str = """jinja
    <header> 
        {{aa}}
    </header>
    """
#print(isinstance(tag_str, TagStr('header')))
#print(issubclass(TagStr('tag-name'),  JinjaStr))
print(isinstance(my_tag_component, Component))
#print(issubclass(Tag('tag-name'), Component))
print(isinstance(my_tag_component, Tag('header')))
