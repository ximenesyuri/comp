from app.main import *
from app.service import build, render, style
from app.mods.helper import Page
from typed import *

@typed
def h1(y: Str) -> TagStr('h1'):
    return """jinja
    <h1 class="pt-20px fz-30px fs-it phone:bg-[#000000]">
        {{ y }}
    </h1>
"""

@typed
def definer(x: Str, depends_on: List(Definer)=[definer_1,]) -> Jinja:
    return """jinja
<html>
<head>
</head>
<body></body>
    {{ definer_1(y)}}
    <p class="fc-[#123123] mt-10em bg-[#000000] mt-10em">
    {{ x }}
    </p>

</html>
"""

page = {
    "definer": definer,
    "context": {"x": "aaaa", "y": "dsadas"},
    "auto_style": True
}

print(render(style(page)))
