from app.main import *
from app.components import div, button
from app.components.buttons import button_close
from app.components.icons.line import icon_search
from app.service import preview, render, mock

component = COMPONENT(
    definer=div * (button * icon_search),
    context={}
)

print(render(component))
