from typed import typed, Str, Bool, List, Json
from typed.models import Model, Optional

Alpine = Model(
    x_init=Optional(Str, ""),
    x_data=Optional(Json, {}),
    x_show=Optional(Str, ""),
    x_cloak=Optional(Bool, False)
)

Div = Model(
    div_id=Optional(Str, "div"),
    div_class=Optional(Str, ""),
    div_hover=Optional(Str, "")
)

Button = Model(
    button_id=Optional(Str, "button"),
    button_class=Optional(Str, ""),
    button_hover=Optional(Str, ""),
    on_click=Optional(Str, ""),
    click_away=Optional(Str, "")
)
