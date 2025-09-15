from typed import Str, Any, List, Enum
from typed.models import optional
from comp.models.base import Globals, Aria
from comp.models.content import Link

@optional
class Item:
    globals:    Globals=Globals()
    aria:       Aria=Aria()
    item_id:    Str="item"
    item_class: Str
    item_style: Str
    item_inner: Any

@optional
class Unordered:
    globals:  Globals=Globals()
    aria:     Aria=Aria()
    ul_id:    Str="ul"
    ul_class: Str
    ul_style: Str
    ul_items: List(Item)

@optional
class Ordered:
    globals:  Globals=Globals()
    aria:     Aria=Aria()
    ol_id:    Str
    ol_class: Str
    ol_style: Str
    ol_items: List(Item)

@optional
class NavItem:
    globals:    Globals=Globals()
    aria:       Aria=Aria()
    item_id:    Str="item"
    item_class: Str
    item_style: Str
    item_inner: Any
    item_link:  Link

@optional
class Nav:
    globals:       Globals=Globals()
    aria:          Aria=Aria()
    nav_id:        Str="nav"
    nav_class:     Str
    nav_style:     Str
    nav_direction: Enum(Str, "vertical", "horizontal")="horizontal"
    nav_items:     List(NavItem)
    ul_id:         Str="nav-ul"
    ul_class:      Str
    ul_style:      Str="list-style: none;"
