from app.main import *
from app.models import Script, Asset, Link
from app.components import link
from app.mods.service import render, preview, mock

@static
def test(content: Content, x: Str) -> Jinja:
    return """jinja
    {{ content}}{{x}}        
"""

print(render(
    link,
    inner="my_link",
    link=Link(link_class="mt-10px"),
    __scripts__=[Script(script_src="https://aaaaaa")],
    __assets__=[Asset(asset_href="/home/yx/files/dev/vor/controller/controller/app/frontend/static/css/basic.css")],
    __minified__=True
    )
)
