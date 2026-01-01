from typed import optional, Str, Bool, Float, Any, Enum
from utils.types import HEX, PathUrl
from comp.models.base import Globals, Aria

@optional
class Button:
    button_globals:    Globals
    button_aria:       Aria
    button_id:         Str="button"
    button_class:      Str
    button_style:      Str
    button_type:       Enum(Str, "button", "reset", "submmit")="button"
    button_on_click:   Str
    button_click_away: Str
    button_inner:      Any

Button.__display__ = "Button"

@optional
class Icon:
    icon_globals: Globals
    icon_aria:    Aria
    icon_id:      Str="icon"
    icon_class:   Str
    icon_style:   Str
    icon_size:    Str="24px"
    icon_fill:    HEX="#000000"
    icon_viewbox: Str="0 -960 960 960"
    icon_stroke:  Float=0.5

Icon.__display__ = "Icon"

@optional
class Image:
    img_globals: Globals
    img_aria:    Aria
    img_id:      Str="img"
    img_class:   Str
    img_style:   Str
    img_alt:     Str
    img_src:     PathUrl=""
    img_lazy:    Bool=True
Img = Image

Image.__display__ = "Image"

@optional
class Text:
    text_globals: Globals
    text_aria:    Aria
    text_id:      Str="text"
    text_class:   Str
    text_style:   Str
    text_inner:   Any

Text.__display__ = "Text"

@optional
class Title:
    title_globals: Globals
    title_aria:    Aria
    title_id:      Str="title"
    title_class:   Str
    title_style:   Str
    title_tag:     Enum(Str, "h1", "h2", "h3", "h4", "h5", "h6")="h1"
    title_inner:   Any

Title.__display__ = "Title"

@optional
class Link:
    link_globals:  Globals
    link_aria:     Aria
    link_id:       Str="link"
    link_class:    Str
    link_style:    Str
    link_href:     PathUrl
    link_target:   Enum(Str, "_self", "_blank", "_parent", "_top")="_self"
    link_rel:      Enum(Str, 'nofollow', 'noopener', 'noreferrer', 'sponsored', 'ugc')
    link_download: PathUrl
    link_inner:    Any

Link.__display__ = "Link"

@optional
class Figure:
    figure_globals: Globals
    figure_aria:    Aria
    figure_img:     Image
    figure_caption: Str

Figure.__display__ = "Figure"

@optional
class Logo:
    logo_globals: Globals
    logo_aria:    Aria
    logo_img:     Image
    logo_link:    Link=Link(link_href="/")

Logo.__display__ = "Logo"
