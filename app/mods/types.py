from typed import Bool
from typed.models import Model
from app.mods.factories import Tag, TagDefiner, TAG
from app.mods.helper import (
    Jinja,
    Markdown,
    Content,
    Definer,   
    COMPONENT,
    STATIC,
    PAGE,
    STATIC_PAGE
)

# ---------------------------
#    CONTENT STRING TYPES
# ---------------------------
Head   = Tag('head')
Body   = Tag('body')
Header = Tag('header')
Footer = Tag('footer')
Aside  = Tag('aside')
Div    = Tag('div')
Button = Tag('button')

Jinja.__display__  = "Jinja"
Head.__display__   = "Head"
Body.__display__   = "Body"
Header.__display__ = "Header"
Footer.__display__ = "Header"
Aside.__display__  = "Aside"
Markdown.__display__  = "Markdown"

# ---------------------------
#       DEFINER TYPES
# ---------------------------
HeadDefiner   = TagDefiner('head')
BodyDefiner   = TagDefiner('body')
HeaderDefiner = TagDefiner('header')
FooterDefiner = TagDefiner('footer')
AsideDefiner  = TagDefiner('aside')

Definer.__display__       = "Definer"
HeadDefiner.__display__   = "HeadDefiner"
BodyDefiner.__display__   = "BodyDefiner"
HeaderDefiner.__display__ = "HeaderDefiner"
FooterDefiner.__display__ = "FooterDefiner"
AsideDefiner.__display_   = "AsideDefiner"

# ---------------------------
#       COMPONENT TYPES
# ---------------------------
HEAD   = TAG('head')
BODY   = TAG('body')
HEADER = TAG('header')
FOOTER = TAG('footer')
ASIDE  = TAG('left-sidebar')

COMPONENT.__display__ = "COMPONENT"
STATIC.__display__    = "STATIC"
HEAD.__display__      = "HEAD"
BODY.__display__      = "BODY"
HEADER.__display__    = "HEADER"
FOOTER.__display__    = "FOOTER"
ASIDE.__display__     = "ASIDE"

# ---------------------------
#       PAGE TYPES
# ---------------------------
PAGE.__display__       = "PAGE"
STATIC_PAGE.__display__ = "STATIC_PAGE"

# ---------------------------
#       OTHER TYPES
# ---------------------------
Context = Model()
