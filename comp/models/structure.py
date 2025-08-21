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

@optional
class Flex:
    globals:        Globals=Globals()
    aria:           Aria=Aria()
    flex_id:        Str
    flex_class:     Str="display: flex"
    flex_style:     Str
    flex_direction: Enum(Str, 'row', 'column')

@optional
class Inline:
    globals:      Globals=Globals()
    aria:         Aria=Aria()
    inline_id:    Str
    inline_class: Str="display: inline"
    inline_style: Str

@optional
class Block:
    globals:      Globals=Globals()
    aria:         Aria=Aria()
    inline_id:    Str
    inline_class: Str="display: block"
    inline_style: Str

@optional
class Header:
    globals:      Globals=Globals()
    aria:         Aria=Aria()
    header_id:    Str="header"
    header_class: Str
    header_style: Str
    header_inner: Any

@optional
class Aside:
    globals:     Globals=Globals()
    aria:        Aria=Aria()
    aside_id:    Str="aside"
    aside_class: Str
    aside_style: Str
    aside_inner: Any

@optional
class Sidebar:
    globals:       Globals=Globals()
    aria:          Aria=Aria()
    sidebar_id:    Str="sidebar"
    sidebar_class: Str
    sidebar_style: Str
    sidebar_inner: Any

@optional
class Column:
    globals:   Globals=Globals()
    aria:      Aria=Aria()
    col_id:    Str
    col_class: Str
    col_style: Str
    col_inner: Any
Col = Column

@optional
class Row:
    globals:   Globals=Globals()
    aria:      Aria=Aria()
    row_id:    Str
    row_class: Str
    row_style: Str
    row_cols:  List(Column)

@optional
class Grid:
    globals:    Globals=Globals()
    aria:       Aria=Aria()
    grid_id:    Str
    grid_class: Str
    grid_style: Str
    grid_rows:  List(Row)
