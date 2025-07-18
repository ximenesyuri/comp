from app.main import *
from app.models import Script, Asset
from app.components import link
from app.mods.service import render

@static
def test(content: Content, x: Str) -> Jinja:
    return """jinja
    {{ content}}{{x}}        
"""

print(render(link, __scripts__=[Script(script_src="https://aaaaaa")], __assets__=[Asset(asset_href="https://bbbbbbb")]))
