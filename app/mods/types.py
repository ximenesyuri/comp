from typed import Bool
from typed.models import Model
from app.mods.factories import TagStr, TagDefiner, Tag
from app.mods.helper import (
    Jinja,
    Markdown,
    Content,
    Definer,
    Component,
    Static,
    Page,
    StaticPage
)

# ---------------------------
#    CONTENT STRING TYPES
# ---------------------------
HeadStr   = TagStr('head')
BodyStr   = TagStr('body')
HeaderStr = TagStr('header')
FooterStr = TagStr('footer')
AsideStr  = TagStr('aside')

Jinja.__display__  = "Jinja"
HeadStr.__display__   = "HeadStr"
BodyStr.__display__   = "BodyStr"
HeaderStr.__display__ = "HeaderStr"
FooterStr.__display__ = "HeaderStr"
AsideStr.__display__  = "AsideStr"
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
Head   = Tag('head')
Body   = Tag('body')
Header = Tag('header')
Footer = Tag('footer')
Aside  = Tag('left-sidebar')

Component.__display__ = "Component"
Static.__display__    = "Static"
Head.__display__      = "Head"
Body.__display__      = "Body"
Header.__display__    = "Header"
Footer.__display__    = "Footer"
Aside.__display__     = "Aside"

# ---------------------------
#       PAGE TYPES
# ---------------------------
Page.__display__       = "Page"
StaticPage.__display__ = "StaticPage"

# ---------------------------
#       OTHER TYPES
# ---------------------------
Context = Model()
