from app.main import *
from app.models import Script, Asset, Link, Unordered, Item, Nav, NavItem
from app.components import ul, nav, link
from app.mods.service import render, preview, mock

nav_ = Nav(
        nav_id="menu-header",
        nav_class="mt-20px",
        ul_class="i:p-10px gap-10px hover:bg-#000000",
        nav_direction="horizontal",
        nav_items=[
            NavItem(
                item_id="item-1",
                item_class="fc-#123123",
                item_link=Link(link_href="https://google.com", inner="link google")
            ),
            NavItem(
                item_id="item-2",
                item_class="fc-#ffffff",
                item_link=Link(href="https://aaa", inner="vvvvvv")
            )
        ]
    )

print(render(nav, nav=nav_, __minified__=True))
preview(nav, nav=nav_)
