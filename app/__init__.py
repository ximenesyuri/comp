from typed import *
from app.main import *
from app.mods.factories import Free

@definer
def test(x: Str) -> Jinja:
    return """jinja
    {{x}} {{y}} 
"""

print(isinstance(test, Free('z', 'y')))
