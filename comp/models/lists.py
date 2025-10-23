from typed import Str, Any, List, Enum
from typed.models import optional
from comp.models.base import Globals, Aria
from comp.models.content import Link

@optional
class Item:
    item_globals: Globals=Globals()
    item_aria:    Aria=Aria()
    item_id:      Str="item"
    item_class:   Str
    item_style:   Str
    item_inner:   Any

Item.__display__ = "Item"

@optional
class Unordered:
    ul_globals: Globals=Globals()
    ul_aria:    Aria=Aria()
    ul_id:      Str="ul"
    ul_class:   Str
    ul_style:   Str
    ul_items:   List(Item)
Ul = Unordered

Unordered.__display__ = "Unordered"

@optional
class Ordered:
    ol_globals: Globals=Globals()
    ol_aria:    Aria=Aria()
    ol_id:      Str
    ol_class:   Str
    ol_style:   Str
    ol_items:   List(Item)
Ol = Ordered

Ordered.__display__ = "Ordered"

@optional
class NavItem(Item):
    item_link: Link

NavItem.__display__ = "NavItem"

@optional
class CustomNav:
    nav_globals:   Globals=Globals()
    nav_aria:      Aria=Aria()
    nav_id:        Str="nav"
    nav_class:     Str
    nav_style:     Str
    nav_direction: Enum(Str, "vertical", "horizontal")="horizontal"
    ul_id:         Str="nav-ul"
    ul_class:      Str
    ul_style:      Str="list-style: none;"

CustomNav.__display__ = "CustomNav"

@optional
class Nav(CustomNav):
    nav_items:     List(NavItem)

Nav.__display__ = "Nav"
