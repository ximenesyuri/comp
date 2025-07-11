from app.mods.factories.base import Tag, TagDefiner, TAG

# ---------------------------
#    CONTENT STRING TYPES
# ---------------------------
Head   = Tag('head')
Body   = Tag('body')
Header = Tag('header')
Footer = Tag('footer')
Aside  = Tag('aside')

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

HEAD.__display__      = "HEAD"
BODY.__display__      = "BODY"
HEADER.__display__    = "HEADER"
FOOTER.__display__    = "FOOTER"
ASIDE.__display__     = "ASIDE"
