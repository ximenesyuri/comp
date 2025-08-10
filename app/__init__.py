from app.main import *
from app.components import  nav, text, link
from app.models import Nav, NavItem, Link

nav_2 = copy(nav, nav="nav_2")

print(eval(text, inner="aaa").jinja)

#print(render(nav_2, nav_2=Nav(nav_items=[NavItem(item_link=Link(link_inner="aaaaaa"))])))
