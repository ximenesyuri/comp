from typed import Str, Bool, Float, HEX, Any, PathUrl, Enum
from typed.models import optional
from comp.models.base import Globals, Aria

@optional
class Button:
    button_globals:    Globals=Globals()
    button_aria:       Aria=Aria()
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
    icon_globals: Globals=Globals()
    icon_aria:    Aria=Aria()
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
    img_globals: Globals=Globals()
    img_aria:    Aria=Aria()
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
    text_globals: Globals=Globals()
    text_aria:    Aria=Aria()
    text_id:      Str="text"
    text_class:   Str
    text_style:   Str
    text_inner:   Any

Text.__display__ = "Text"

@optional
class Title:
    title_globals: Globals=Globals()
    title_aria:    Aria=Aria()
    title_id:      Str="title"
    title_class:   Str
    title_style:   Str
    title_tag:     Enum(Str, "h1", "h2", "h3", "h4", "h5", "h6")="h1"
    title_inner:   Any

Title.__display__ = "Title"

@optional
class Link:
    link_globals:  Globals=Globals()
    link_aria:     Aria=Aria()
    link_id:       Str="link"
    link_class:    Str
    link_style:    Str
    link_href:     PathUrl="https://"
    link_target:   Enum(Str, "_self", "_blank", "_parent", "_top")="_self"
    link_rel:      Enum(Str, 'nofollow', 'noopener', 'noreferrer', 'sponsored', 'ugc')
    link_download: PathUrl=""
    link_inner:    Any

Link.__display__ = "Link"

@optional
class Figure:
    figure_globals: Globals=Globals()
    figure_aria:    Aria=Aria()
    figure_img:     Image=Image()
    figure_caption: Str

Figure.__display__ = "Figure"

@optional
class Logo:
    logo_globals: Globals=Globals()
    logo_aria:    Aria=Aria()
    logo_img:     Image=Image()
    logo_link:    Link=Link(link_href="/")

Logo.__display__ = "Logo"
