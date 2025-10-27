from comp.mods.decorators import component
from comp.mods.types.base import Jinja, Inner
from comp.mods.err import ComponentErr
from comp.models.structure import Div, Header, Column, Row, Grid, Aside, Footer, Head, Main, Body, Page
from comp.mods.helper.comps import (
    if_div,
    if_header,
    if_col,
    if_row,
    if_grid,
    if_footer,
    if_aside,
    if_head,
    if_main,
    if_body,
    if_page,
    _render_inner
)
from comp.comps.includes import asset, script

@component
def header(header: Header=Header(), inner: Inner="") -> Jinja:
    try:
        if header.header_inner:
            rendered_inner = _render_inner(header.header_inner)
        elif inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""
        return f"""jinja
<header{ if_header(header) }>{ rendered_inner }</header>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def aside(aside: Aside=Aside(), inner: Inner="") -> Jinja:
    try:
        if aside.aside_inner:
            rendered_inner = _render_inner(aside.aside_inner)
        elif inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""
        return f"""jinja
<aside{ if_aside(aside) }>{ rendered_inner }</aside>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def footer(footer: Footer=Footer(), inner: Inner="") -> Jinja:
    try:
        if footer.footer_inner:
            rendered_inner = _render_inner(footer.footer_inner)
        elif inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""
        return f"""jinja
<footer{ if_footer(footer) }>{ rendered_inner }</footer>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def head(head: Head=Head(), inner: Inner="", __context__={"asset": asset, "script": script}) -> Jinja:
    try:
        if head.head_inner:
            rendered_inner = _render_inner(head.head_inner)
        elif inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""
        from comp.mods.helper.comps  import _generate_meta_tags
        if head.head_meta:
            meta_tags = _generate_meta_tags(head.head_meta)
        else:
            meta_tags = ""
        return f"""jinja
<head{ if_head(head) }>
    { meta_tags }
    [% if head.head_assets is defined and head.head_assets %][% for a in head.head_assets %]
    [[ asset(asset=a) ]][% endfor %][% endif %]
    [% if head.head_scripts is defined and head.head_scripts %][% for s in head.head_scripts %]
    [[ script(script=s) ]][% endfor %][% endif %]
    { rendered_inner }
</head>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def main(main: Main=Main(), inner: Inner="") -> Jinja:
    try:
        if main.main_inner:
            rendered_inner = _render_inner(main.main_inner)
        elif inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""
        return f"""jinja
<main{ if_main(main) }>{ rendered_inner }</main>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def body(body: Body=Body(), inner: Inner="", __context__={"header": header, "aside": aside, "main": main, "footer": footer}) -> Jinja:
    try:
        if body.body_inner:
            rendered_inner = _render_inner(body.body_inner)
        elif inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""

        return f"""jinja
<body{ if_body(body) }>
    [% if body.body_header is defined and body.body_header %][[ header(header=body.body_header) ]][% endif %]
    [% if body.body_asides is defined and body.body_asides %][% for a in body.body_asides %]
    [[ aside(aside=a) ]][% endfor %][% endif %]
    [% if body.body_main is defined and body.body_main %][[ main(main=body.body_main) ]][% endif %]
    { rendered_inner }
    [% if body.body_footer is defined and body.body_footer %][[ footer(footer=body.body_footer) ]][% endif %]
</body>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def page(page: Page=Page(), inner: Inner="", __context__={"head": head, "body": body}) -> Jinja:
    try:
        if page.page_inner:
            rendered_inner = _render_inner(page.page_inner)
        elif inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""
        return f"""jinja
<!DOCTYPE html>
<html{ if_page(page) }>
    [% if page.page_head is defined and page.page_head %][[ head(head=page.page_head) ]][% endif %]
    [% if page.page_body is defined and page.page_body %][[ body(body=page.page_body) ]][% endif %]
    { rendered_inner }
</html>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def div(div: Div=Div(), inner: Inner="") -> Jinja:
    try:
        if div.div_inner:
            rendered_inner = _render_inner(div.div_inner)
        elif inner:
            rendered_inner = _render_inner(inner)
        else:
            rendered_inner = ""
        return f"""jinja
<div{ if_div(div) }>{ rendered_inner }</div>
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def col(col: Column=Column(), inner: Inner="") -> Jinja:
    try:
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
    except Exception as e:
        raise ComponentErr(e)

@component
def col_1(col: Column=Column(), inner: Inner="") -> Jinja:
    try:
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
    except Exception as e:
        raise ComponentErr(e)

@component
def col_2(col: Column=Column(), inner: Inner="") -> Jinja:
    try:
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
    except Exception as e:
        raise ComponentErr(e)

@component
def col_3(col: Column=Column(), inner: Inner="") -> Jinja:
    try:
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
    except Exception as e:
        raise ComponentErr(e)

@component
def col_4(col: Column=Column(), inner: Inner="") -> Jinja:
    try:
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
    except Exception as e:
        raise ComponentErr(e)

@component
def col_5(col: Column=Column(), inner: Inner="") -> Jinja:
    try:
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
    except Exception as e:
        raise ComponentErr(e)

@component
def row(row: Row=Row(), __context__={"col": col}) -> Jinja:
    try:
        existing = row.row_class or ""
        if "row" not in existing.split():
            row.row_class = (existing + " row").strip()
        return f"""jinja
<div{ if_row(row) }>[% if row.row_cols is defined %][% for c in row.row_cols %]
    [[ col(col=c) ]][% endfor %]
</div>[% else %]</div>[% endif %]
"""
    except Exception as e:
        raise ComponentErr(e)

@component
def grid(grid: Grid=Grid(), __context__={"row": row}) -> Jinja:
    try:
        return f"""jinja
<div{ if_grid(grid) }>[% if grid.grid_rows is defined %][% for r in grid.grid_rows %]
    [[ row(row=r) ]][% endfor %]
</div>[% else %]</div>[% endif %]
"""
    except Exception as e:
        raise ComponentErr(e)
