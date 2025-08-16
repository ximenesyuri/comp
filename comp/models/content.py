from typed import Str, Bool, Float, HEX, Any, PathUrl, Enum
from typed.models import optional
from comp.models.base import Globals, Aria

@optional
class Button:
    globals:      Globals
    aria:         Aria
    button_id:    Str="button"
    button_class: Str
    button_style: Str
    button_type:  Enum(Str, "button", "reset", "submmit")="button"
    on_click:     Str
    click_away:   Str
    button_inner: Any

@optional
class Icon:
    globals:      Globals
    icon_id:      Str="icon"
    icon_class:   Str
    icon_size:    Str="24px"
    icon_fill:    HEX="#000000"
    icon_viewbox: Str="0 -960 960 960"
    icon_stroke:  Float=0.5

@optional
class Image:
    globals:   Globals
    aria:      Aria
    img_id:    Str="img"
    img_class: Str
    img_style: Str
    img_alt:   Str
    img_src:   PathUrl=""
    img_lazy:  Bool=True
Img = Image

@optional
class Text:
    globals:    Globals
    aria:       Aria
    text_id:    Str="text"
    text_class: Str
    text_style: Str
    text_inner: Any

@optional
class Title:
    globals:     Globals
    aria:        Aria
    title_id:    Str="title"
    title_class: Str
    title_style: Str
    title_tag:   Enum(Str, "h1", "h2", "h3", "h4", "h5", "h6")="h1"
    title_inner: Any

@optional
class Link:
    globals:       Globals
    aria:          Aria
    link_id:       Str="link"
    link_class:    Str
    link_style:    Str
    link_href:     PathUrl="https://"
    link_target:   Enum(Str, "_self", "_blank", "_parent", "_top")="_self"
    link_rel:      Enum(Str, 'nofollow', 'noopener', 'noreferrer', 'sponsored', 'ugc', "")
    link_download: PathUrl
    link_inner:    Any

@optional
class Figure:
    globals:        Globals
    aria:           Aria
    figure_img:     Image
    figure_caption: Str

@optional
class Logo:
    globals:   Globals
    aria:      Aria
    logo_img:  Image
    logo_link: Link=Link(link_href="/")
