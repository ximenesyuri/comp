from app.main import *
from app.service import build, render
from app.mods.helper import Page
from typed import *

@typed
def definer(x: Str) -> JinjaStr:
    return """jinja
<html>
<head>
</head>
<body></body>
    <{{ x }} class="mt-10px">
    </{{x }}>
</html>
    """  

page = {
    "definer": definer,
    "context": {"x": "aaaa", "y": 12},
    "auto_style": True
}

print(isinstance(page, Page))
