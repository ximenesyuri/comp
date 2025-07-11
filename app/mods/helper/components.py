from typed import typed, Str, Any, Maybe
from app.models import Div

@typed
def _if(entry: Any=None, what: Str="id") -> Maybe(Str):
    if entry:
        f"{{% if {entry} %}}{what}=\"{{{{{entry}}}}}\"{{% endif %}}"

@typed
def if_id(entry: Any=None) -> Maybe(Str):
    return _if(entry, "id")

@typed
def if_class(entry: Any=None) -> Maybe(Str):
    return _if(entry, 'class')

@typed
def if_hover(entry: Any=None) -> Maybe(Str):
    return _if(entry, "hover")

@typed
def if_div(div: Div={}) -> Maybe(Str):
    if div:
        return f"{if_id(div.div_id)} {if_class(div.div_class)} {if_hover(div.div_hover)}"
