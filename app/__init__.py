from app.main import *
from app.mods.comp import render
from typed import typed, Str


def test() -> JinjaStr:
    return """jinja
        {{a}}
    """

def function(x: Str, depends_on=[test]) -> JinjaStr:
    return """jinja 
        <{{x}}> aaaa {{y}} {{test()}} </{{x}}>
    """

component = {
    "definer": function,
    "context": {'a': 'dddddd', 'y': 'xxxxxx'}
}    

print(isinstance(component, Component))
print(render(component))
