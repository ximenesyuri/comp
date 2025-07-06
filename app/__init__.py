from app.main import *
from app.components import div, button
from app.service import render

component = COMPONENT(
    definer=div + button,
    context={}
)

print(render(component))

