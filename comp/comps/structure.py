from comp.mods.decorators import component
from comp.mods.types.base import Jinja, Inner
from comp.models.structure import Div, Header, Column, Row, Grid, Aside
from comp.mods.helper.comps import if_div, if_header, if_col, if_row, if_grid

@component
def header(header: Header=Header(), inner: Inner="") -> Jinja:
    return f"""jinja
<div{ if_header(header) }>[% if header.header_inner %]
    { header.header_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def aside(aside: Aside=Aside(), inner: Inner="") -> Jinja:
    return f"""jinja
<div{ if_aside(aside) }>[% if aside.aside_inner %]
    { aside.aside_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def div(div: Div=Div(), inner: Inner="") -> Jinja:
    div_data    = if_div(div)
    return f"""jinja
<div{ div_data }>[% if div.div_inner %]
    { div.div_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def col(col: Column=Column(), inner: Inner="") -> Jinja:
    existing = col.col_class or ""
    if "col" not in existing.split():
        col.col_class = (existing + " col").strip()
    col_data = if_col(col)
    return f"""jinja
<div{ col_data }>[% if col.col_inner %]
    { col.col_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def col_1(col: Column=Column(), inner: Inner="") -> Jinja:
    existing = col.col_class or ""
    if "col-1" not in existing.split():
        col.col_class = (existing + " col-1").strip()
    col_data = if_col(col)
    return f"""jinja
<div{ col_data }>[% if col.col_inner %]
    { col.col_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def col_2(col: Column=Column(), inner: Inner="") -> Jinja:
    existing = col.col_class or ""
    if "col-2" not in existing.split():
        col.col_class = (existing + " col-2").strip()
    col_data = if_col(col)
    return f"""jinja
<div{ col_data }>[% if col.col_inner %]
    { col.col_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def col_3(col: Column=Column(), inner: Inner="") -> Jinja:
    existing = col.col_class or ""
    if "col-3" not in existing.split():
        col.col_class = (existing + " col-3").strip()
    col_data = if_col(col)
    return f"""jinja
<div{ col_data }>[% if col.col_inner %]
    { col.col_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def col_4(col: Column=Column(), inner: Inner="") -> Jinja:
    existing = col.col_class or ""
    if "col-4" not in existing.split():
        col.col_class = (existing + " col-4").strip()
    col_data = if_col(col)
    return f"""jinja
<div{ col_data }>[% if col.col_inner %]
    { col.col_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def col_5(col: Column=Column(), inner: Inner="") -> Jinja:
    existing = col.col_class or ""
    if "col-5" not in existing.split():
        col.col_class = (existing + " col-5").strip()
    col_data = if_col(col)
    return f"""jinja
<div{ col_data }>[% if col.col_inner %]
    { col.col_inner }
</div>[% elif inner is defined %]
    { inner }
</div>[% else %]</div>[% endif %]
"""

@component
def row(row: Row=Row(), __context__={"col": col}) -> Jinja:
    existing = row.row_class or ""
    if "row" not in existing.split():
        row.row_class = (existing + " row").strip()
    row_data = if_row(row)
    return f"""jinja
<div{ row_data }>[% if row.row_cols %][% for c in row.row_cols %]
    [[ col(col=c) ]][% endfor %]
</div>[% else %]</div>[% endif %]
"""

@component
def grid(grid: Grid=Grid(), __context__={"row": row}) -> Jinja:
    grid_data = if_grid(grid)
    return f"""jinja
<div{ grid_data }>[% if grid.grid_rows %][% for r in grid.grid_rows %]
    [[ row(row=r) ]][% endfor %]
</div>[% else %]</div>[% endif %]
"""
