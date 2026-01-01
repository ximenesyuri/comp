from utils.general import lazy

__imports__ = {
    "icon_search": "comp.comps.icons.line",
    "icon_close": "comp.comps.icons.line",
    "icon_menu": "comp.comps.icons.line",
    "icon_home": "comp.comps.icons.line",
    "icon_theme_switcher": "comp.comps.icons.line"
}

if lazy(__imports__):
    from comp.comps.icons.line import (
        icon_search, icon_close,
        icon_menu, icon_home,
        icon_theme_switcher
    )
