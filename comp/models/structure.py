from typed import Str, Any, Enum, List
from typed.models import optional
from comp.models.base import Globals, Aria

@optional
class Div:
    div_globals: Globals=Globals()
    div_aria:    Aria=Aria()
    div_id:      Str
    div_class:   Str
    div_style:   Str
    div_inner:   Any

Div.__display__ = "Div"

@optional
class Flex(Div):
    div_class:     Str='display: flex'
    div_direction: Enum(Str, 'row', 'column')

Flex.__display__ = "Flex"

@optional
class Inline(Div):
    div_class: Str="display: inline"

Inline.__display__ = "Inline"

@optional
class Block(Div):
    div_class: Str="display: block"

Block.__display__ = "Block"

@optional
class Header:
    header_globals: Globals=Globals()
    header_aria:    Aria=Aria()
    header_id:      Str="header"
    header_class:   Str
    header_style:   Str
    header_inner:   Any

Header.__display__ = "Header"

@optional
class Footer:
    footer_globals: Globals=Globals()
    footer_aria:    Aria=Aria()
    footer_id:      Str="footer"
    footer_class:   Str
    footer_style:   Str
    footer_inner:   Any

Footer.__display__ = "Footer"

@optional
class Aside:
    aside_globals: Globals=Globals()
    aside_aria:    Aria=Aria()
    aside_id:      Str="aside"
    aside_class:   Str
    aside_style:   Str
    aside_inner:   Any

Aside.__display__ = "Aside"

@optional
class Sidebar:
    sidebar_globals: Globals=Globals()
    sidebar_aria:    Aria=Aria()
    sidebar_id:      Str="sidebar"
    sidebar_class:   Str
    sidebar_style:   Str
    sidebar_inner:   Any

Sidebar.__display__ = "Sidebar"

@optional
class Column:
    col_globals: Globals=Globals()
    col_aria:    Aria=Aria()
    col_id:      Str
    col_class:   Str
    col_style:   Str
    col_inner:   Any
Col = Column

Column.__display__ = "Column"

@optional
class Row:
    row_globals: Globals=Globals()
    row_aria:    Aria=Aria()
    row_id:      Str
    row_class:   Str
    row_style:   Str
    row_cols:    List(Column)

Row.__display__ = "Row"

@optional
class Grid:
    grid_globals: Globals=Globals()
    grid_aria:    Aria=Aria()
    grid_id:      Str
    grid_class:   Str
    grid_style:   Str
    grid_rows:    List(Row)

Grid.__display__ = "Grid"
