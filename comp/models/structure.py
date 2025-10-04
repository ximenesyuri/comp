from typed import Str, Any, Enum, List, Maybe
from typed.models import optional
from comp.models.base import Globals, Aria

@optional
class Div:
    globals:   Globals=Globals()
    aria:      Aria=Aria()
    div_id:    Str
    div_class: Str
    div_style: Str
    div_inner: Any

Div.__display__ = "Div"

@optional
class Flex:
    globals:        Globals=Globals()
    aria:           Aria=Aria()
    flex_id:        Str
    flex_class:     Str="display: flex"
    flex_style:     Str
    flex_direction: Enum(Str, 'row', 'column')

Flex.__display__ = "Flex"

@optional
class Inline:
    globals:      Globals=Globals()
    aria:         Aria=Aria()
    inline_id:    Str
    inline_class: Str="display: inline"
    inline_style: Str

Inline.__display__ = "Inline"

@optional
class Block:
    globals:      Globals=Globals()
    aria:         Aria=Aria()
    inline_id:    Str
    inline_class: Str="display: block"
    inline_style: Str

Block.__display__ = "Block"

@optional
class Header:
    globals:      Globals=Globals()
    aria:         Aria=Aria()
    header_id:    Str="header"
    header_class: Str
    header_style: Str
    header_inner: Any

Header.__display__ = "Header"

@optional
class Footer:
    globals:      Globals=Globals()
    aria:         Aria=Aria()
    footer_id:    Str="footer"
    footer_class: Str
    footer_style: Str
    footer_inner: Any

Footer.__display__ = "Footer"

@optional
class Aside:
    globals:     Globals=Globals()
    aria:        Aria=Aria()
    aside_id:    Str="aside"
    aside_class: Str
    aside_style: Str
    aside_inner: Any

Aside.__display__ = "Aside"

@optional
class Sidebar:
    globals:       Globals=Globals()
    aria:          Aria=Aria()
    sidebar_id:    Str="sidebar"
    sidebar_class: Str
    sidebar_style: Str
    sidebar_inner: Any

Sidebar.__display__ = "Sidebar"

@optional
class Column:
    globals:   Globals=Globals()
    aria:      Aria=Aria()
    col_id:    Str
    col_class: Str
    col_style: Str
    col_inner: Any
Col = Column

Column.__display__ = "Column"

@optional
class Row:
    globals:   Globals=Globals()
    aria:      Aria=Aria()
    row_id:    Str
    row_class: Str
    row_style: Str
    row_cols:  List(Column)

Row.__display__ = "Row"

@optional
class Grid:
    globals:    Globals=Globals()
    aria:       Aria=Aria()
    grid_id:    Str
    grid_class: Str
    grid_style: Str
    grid_rows:  List(Row)

Grid.__display__ = "Grid"
