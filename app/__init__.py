from app.main import *
from app.models import Script, Asset, Link, Unordered, Item, Nav, NavItem
from app.components import ul, nav, link
from app.mods.service import render, preview, mock

nav_ = Nav(
        nav_id="axxxx",
        nav_class="mt-20px",
        nav_items=[
            NavItem(
                item_id="xxxxx",
                item_class="pt-5px",
                item_link=Link(link_href="https://aaaaaaa", inner="aaaaaa")
            ),
            NavItem(
                item_id="aaaaaaaaaa",
                item_link=Link(href="https://aaa", inner="vvvvvv")
            )
        ]
    )

print(preview(nav, nav=nav_))
