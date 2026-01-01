from typed import Maybe
from comp.mods.decorators import comp
from comp.mods.types.base import Jinja, Inner
from comp.mods.err import CompErr
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

@comp
def header(header: Maybe(Header)=None, inner: Inner="") -> Jinja:
    try:
        if header is None:
            header = Header()
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
        raise CompErr(e)

@comp
def aside(aside: Maybe(Aside)=None, inner: Inner="") -> Jinja:
    try:
        if aside is None:
            aside = Aside()
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
        raise CompErr(e)

@comp
def footer(footer: Maybe(Footer)=None, inner: Inner="") -> Jinja:
    try:
        if footer is None:
            footer = Footer()
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
        raise CompErr(e)

@comp
def head(head: Maybe(Head)=None, inner: Inner="", __context__={"asset": asset, "script": script}) -> Jinja:
    try:
        if head is None:
            head = Head()
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
        raise CompErr(e)

@comp
def main(main: Maybe(Main)=None, inner: Inner="") -> Jinja:
    try:
        if main is None:
            main = Main()
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
        raise CompErr(e)

@comp
def body(body: Maybe(Body)=None, inner: Inner="", __context__={"header": header, "aside": aside, "main": main, "footer": footer}) -> Jinja:
    try:
        if body is None:
            body = Body()
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
        raise CompErr(e)

@comp
def page(page: Maybe(Page)=None, inner: Inner="", __context__={"head": head, "body": body}) -> Jinja:
    try:
        if page is None:
            page = Page()
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
        raise CompErr(e)

@comp
def div(div: Maybe(Div)=None, inner: Inner="") -> Jinja:
    try:
        if div is None:
            div = Div()
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
        raise CompErr(e)

@comp
def col(col: Maybe(Column)=None, inner: Inner="") -> Jinja:
    try:
        if col is None:
            col = Column()
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
        raise CompErr(e)

@comp
def col_1(col: Maybe(Column)=None, inner: Inner="") -> Jinja:
    try:
        if col is None:
            col = Column()
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
        raise CompErr(e)

@comp
def col_2(col: Maybe(Column)=None, inner: Inner="") -> Jinja:
    try:
        if col is None:
            col = Column()
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
        raise CompErr(e)

@comp
def col_3(col: Maybe(Column)=None, inner: Inner="") -> Jinja:
    try:
        if col is None:
            col = Column()
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
        raise CompErr(e)

@comp
def col_4(col: Maybe(Column)=None, inner: Inner="") -> Jinja:
    try:
        if col is None:
            col = Column()
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
        raise CompErr(e)

@comp
def col_5(col: Maybe(Column)=None, inner: Inner="") -> Jinja:
    try:
        if col is None:
            col = Column()
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
        raise CompErr(e)

@comp
def row(row: Maybe(Row)=None, __context__={"col": col}) -> Jinja:
    try:
        if row is None:
            row = Row()
        existing = row.row_class or ""
        if "row" not in existing.split():
            row.row_class = (existing + " row").strip()
        return f"""jinja
<div{ if_row(row) }>[% if row.row_cols is defined %][% for c in row.row_cols %]
    [[ col(col=c) ]][% endfor %]
</div>[% else %]</div>[% endif %]
"""
    except Exception as e:
        raise CompErr(e)

@comp
def grid(grid: Maybe(Grid)=None, __context__={"row": row}) -> Jinja:
    try:
        if grid is None:
            grid = Grid()
        return f"""jinja
<div{ if_grid(grid) }>[% if grid.grid_rows is defined %][% for r in grid.grid_rows %]
    [[ row(row=r) ]][% endfor %]
</div>[% else %]</div>[% endif %]
"""
    except Exception as e:
        raise CompErr(e)
