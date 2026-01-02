from utils.general import lazy

__imports__ = {
    "jinja":   "comp.mods.decorators",
    "comp":    "comp.mods.decorators",
    "Jinja":   "comp.mods.types.base",
    "Inner":   "comp.mods.types.base",
    "COMP":    "comp.mods.helper.types_",
    "Tag":     "comp.mods.types.factories",
    "TAG":     "comp.mods.types.factories",
    "copy":    "comp.mods.operations",
    "concat":  "comp.mods.operations",
    "join":    "comp.mods.operations",
    "eval":    "comp.mods.operations",
    "render":  "comp.mods.service",
    "mock":    "comp.mods.service",
    "preview": "comp.mods.service",
    "minify":  "comp.mods.service"
}

if lazy(__imports__):
    from comp.mods.decorators import jinja, comp
    from comp.mods.types.base import Jinja, Inner
    from comp.mods.helper.types_ import COMP
    from comp.mods.types.factories import Tag, TAG
    from comp.mods.operations import copy, concat, join, eval
    from comp.mods.service import render, mock, preview, minify
