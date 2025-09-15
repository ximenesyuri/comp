from comp.mods.decorators import component
from comp.mods.types.base import Jinja, Inner
from comp.models.structure import Div, Header, Column, Row, Grid, Aside
from comp.mods.helper.comps import (
    if_div,
    if_header,
    if_col,
    if_row,
    if_grid,
    _render_inner
)

@component
def header(header: Header=Header(), inner: Inner="") -> Jinja:
    if header.header_inner:
        rendered_inner = _render_inner(header.header_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<header{ if_header(header) }>{ rendered_inner }</header>
"""

@component
def aside(aside: Aside=Aside(), inner: Inner="") -> Jinja:
    if aside.aside_inner:
        rendered_inner = _render_inner(aside.aside_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<aside{ if_aside(aside) }>{ rendered_inner }</aside>
"""

@component
def div(div: Div=Div(), inner: Inner="") -> Jinja:
    if div.div_inner:
        rendered_inner = _render_inner(div.div_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<div{ if_div(div) }>{ rendered_inner }</div>
"""

@component
def col(col: Column=Column(), inner: Inner="") -> Jinja:
    existing = col.col_class or ""
    if "col" not in existing.split():
        col.col_class = (existing + " col").strip()
    if col.col_inner:
        rendered_inner = _render_inner(col.col_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<div{ if_col(col) }>{ rendered_inner }</div>
"""

@component
def col_1(col: Column=Column(), inner: Inner="") -> Jinja:
    existing = col.col_class or ""
    if "col-1" not in existing.split():
        col.col_class = (existing + " col-1").strip()
    if col.col_inner:
        rendered_inner = _render_inner(col.col_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<div{ if_col(col) }>{ rendered_inner }</div>
"""

@component
def col_2(col: Column=Column(), inner: Inner="") -> Jinja:
    existing = col.col_class or ""
    if "col-2" not in existing.split():
        col.col_class = (existing + " col-2").strip()
    if col.col_inner:
        rendered_inner = _render_inner(col.col_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<div{ if_col(col) }>{ rendered_inner }</div>
"""

@component
def col_3(col: Column=Column(), inner: Inner="") -> Jinja:
    existing = col.col_class or ""
    if "col-3" not in existing.split():
        col.col_class = (existing + " col-3").strip()
    if col.col_inner:
        rendered_inner = _render_inner(col.col_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<div{ if_col(col) }>{ rendered_inner }</div>
"""

@component
def col_4(col: Column=Column(), inner: Inner="") -> Jinja:
    existing = col.col_class or ""
    if "col-4" not in existing.split():
        col.col_class = (existing + " col-4").strip()
    if col.col_inner:
        rendered_inner = _render_inner(col.col_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<div{ if_col(col) }>{ rendered_inner }</div>
"""

@component
def col_5(col: Column=Column(), inner: Inner="") -> Jinja:
    existing = col.col_class or ""
    if "col-5" not in existing.split():
        col.col_class = (existing + " col-5").strip()
    if col.col_inner:
        rendered_inner = _render_inner(col.col_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<div{ if_col(col) }>{ rendered_inner }</div>
"""

@component
def row(row: Row=Row(), __context__={"col": col}) -> Jinja:
    existing = row.row_class or ""
    if "row" not in existing.split():
        row.row_class = (existing + " row").strip()
    return f"""jinja
<div{ if_row(row) }>[% if row.row_cols is defined %][% for c in row.row_cols %]
    [[ col(col=c) ]][% endfor %]
</div>[% else %]</div>[% endif %]
"""

@component
def grid(grid: Grid=Grid(), __context__={"row": row}) -> Jinja:
    return f"""jinja
<div{ if_grid(grid) }>[% if grid.grid_rows is defined %][% for r in grid.grid_rows %]
    [[ row(row=r) ]][% endfor %]
</div>[% else %]</div>[% endif %]
"""
