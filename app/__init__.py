from typed import *
from app.main import *

@definer
def test(x: Str) -> Jinja:
    return """jinja
    {{x}}
"""

print(isinstance(test, FreeDefiner(-1)))
