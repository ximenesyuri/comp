from app.main import *

@definer
def test_1(x: Str) -> Jinja:
    return """jinja
<aa> {{x}} {{y}} </aa>
"""

print(test_1.jinja_free_vars)

print(isinstance(test_1, FreeDefiner(1)))

@definer
def test_2(x: Str) -> Jinja:
    return """jinja
<bb> {{x}} </bb>
"""

print((test_1 + test_2).jinja)
