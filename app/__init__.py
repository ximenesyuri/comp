from typed import *
from app.main import *
from app.service import render

@definer
def free(x: Str) -> Jinja:
    return """jinja
    {{x}} {{y}}
"""


@definer
def test(z: Str) -> Jinja:
    return """jinja
    </{{ z }}>
"""


aa = concat(free, test)

component = Component(
    definer=aa,
    context={"x": "aaa", "z": "bbbb"}
)

print(render(component))
