from app.main import *
from app.components.icons.line import search_1
from app.service import render, style
from typed import typed, List

component = Component({
    "definer": search_1,
    "context": {
        "size": "23px",
        "fill": "#000000"
    }
})

print(isinstance(component, Component))

@typed
def page_definer(depends_on: List(Definer)=[search_1]) -> Jinja:
    return """jinja
<html>
<head>
</head>
<body>
{{search_1('23px', '#000000')}}
</body>
</html>
"""

page = Page({
    "definer": page_definer,
    "context": {},
    "static_dir": "",
    "auto_style": True
})

print(render(style(page)))
