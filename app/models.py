from typed import typed, Str, Bool, List, Json
from typed.models import Model, Optional

AlpineModel = Model(
    x_init=Optional(Str, ""),
    x_data=Optional(Json, {}),
    x_show=Optional(Str, ""),
    x_cloak=Optional(Bool, False)
)

ElementModel = Model(
    id=Optional(Str, "div"),
    classes=Optional(Str, ""),
    hover=Optional(Str, "")
)

ButtonModel = Model(
    __extends__=ElementModel,
    on_click=Optional(Str, ""),
    click_away=Optional(Str, "")
)
