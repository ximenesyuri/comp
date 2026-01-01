from utils.general import lazy

__imports__ = {
    "GridEntity":    "comp.mods.grid",
    "GridEFactory":  "comp.mods.grid",
    "build_col":     "comp.mods.grid",
    "build_row":     "comp.mods.grid",
    "build_grid":    "comp.mods.grid",
    "build_factory": "comp.mods.grid",
    "build_comp":    "comp.mods.grid"
}

if lazy(__imports__):
    from comp.mods.grid import (
        GridEntity, GridFactory,
        build_col, build_row, build_grid, build_factory, build_comp
    )
