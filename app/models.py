from typed import typed, Str, Bool, List, Json
from typed.models import Model, Optional

Alpine = Model(
    x_init=Optional(Str, ""),
    x_data=Optional(Json, {}),
    x_show=Optional(Str, ""),
    x_cloak=Optional(Bool, False)
)

Div = Model(
    id=Optional(Str, "div"),
    classes=Optional(Str, ""),
    hover=Optional(Str, "")
)

Button = Model(
    id=Optional(Str, "button"),
    classes=Optional(Str, ""),
    hover=Optional(Str, ""),
    on_click=Optional(Str, ""),
    click_away=Optional(Str, "")
)
