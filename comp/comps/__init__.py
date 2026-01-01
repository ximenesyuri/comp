from utils.general import lazy

__imports__ = {
    "button_close": "comp.comps.buttons",
    "button_menu": "comp.comps.buttons",
    "button_search": "comp.comps.buttons",
    "button_home": "comp.comps.buttons",
    "button_theme_switcher": "comp.comps.buttons",
    "text": "comp.comps.content",
    "title": "comp.comps.content",
    "link": "comp.comps.content",
    "image": "comp.comps.content",
    "img": "comp.comps.content",
    "figure": "comp.comps.content",
    "fig": "comp.comps.content",
    "button": "comp.comps.content",
    "logo": "comp.comps.content",
    "alpine": "comp.comps.extensions",
    "search": "comp.comps.extensions",
    "search_script": "comp.comps.extensions",
    "input": "comp.comps.form",
    "script": "comp.comps.includes",
    "asset": "comp.comps.includes",
    "item": "comp.comps.lists",
    "unordered": "comp.comps.lists",
    "ul": "comp.comps.lists",
    "ordered": "comp.comps.lists",
    "ol": "comp.comps.lists",
    "nav": "comp.comps.lists",
    "desktop": "comp.comps.responsive",
    "not_desktop": "comp.comps.responsive",
    "tablet": "comp.comps.responsive",
    "not_tablet": "comp.comps.responsive",
    "phone": "comp.comps.responsive",
    "not_phone": "comp.comps.responsive",
    "mobile": "comp.comps.responsive",
    "not_mobile": "comp.comps.responsive",
    "header": "comp.comps.structure",
    "aside": "comp.comps.structure",
    "footer": "comp.comps.structure",
    "head": "comp.comps.structure",
    "body": "comp.comps.structure",
    "main": "comp.comps.structure",
    "page": "comp.comps.structure",
    "div": "comp.comps.structure",
    "col": "comp.comps.structure",
    "col_1": "comp.comps.structure",
    "col_2": "comp.comps.structure",
    "col_3": "comp.comps.structure",
    "col_4": "comp.comps.structure",
    "col_5": "comp.comps.structure",
    "row": "comp.comps.structure",
    "grid": "comp.comps.structure",
    "content": "comp.comps.special",
    "markdown": "comp.comps.special",
}

if lazy(__imports__):
    from comp.comps.buttons import (
        button_close, button_menu,
        button_search, button_home,
        button_theme_switcher
    )
    from comp.comps.content import (
        text, title, link,
        image, img, figure, fig,
        button, logo
    )
    from comp.comps.extensions import (
        alpine,
        search, search_script
    )
    from comp.comps.form import input
    from comp.comps.includes import script, asset
    from comp.comps.lists import (
        item,
        unordered, ul, ordered, ol,
        nav
    )
    from comp.comps.responsive import (
        desktop, not_desktop,
        tablet, not_tablet,
        phone, not_phone,
        mobile, not_mobile
    )
    from comp.comps.structure import (
        header, aside, footer, head, body, main, page,
        div,
        col, col_1, col_2, col_3, col_4, col_5,
        row, grid
    )
    from comp.comps.special import content, markdown

