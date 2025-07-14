from app.mods.factories.base import Tag, TagDefiner, TAG

# ---------------------------
#    CONTENT STRING TYPES
# ---------------------------

DivTag     = Tag('div')
TextTag    = Tag('p')
TitleTag   = Tag('h1', 'h2', 'h3', 'h4', 'h5', 'h6')
ImageTag   = Tag('img')
LinkTag    = Tag('a')
ScriptTag  = Tag('script')
AssetTag   = Tag('link')
FigureTag  = Tag('figure')
ButtonTag  = Tag('button')
HeadTag    = Tag('head')
BodyTag    = Tag('body')
HeaderTag  = Tag('header')
FooterTag  = Tag('footer')
AsideTag   = Tag('aside')

DivTag.__display__    = "DivTag"
TextTag.__display__   = "TextTag"
TitleTag.__display__  = "TitleTag"
ImageTag.__display__  = "ImageTag"
LinkTag.__display__   = "LinkTag"
ScriptTag.__display_  = "ScriptTag"
AssetTag.__display__  = "AssetTag"
FigureTag.__display__ = "FigureTag"
HeadTag.__display__   = "HeadTag"
BodyTag.__display__   = "BodyTag"
HeaderTag.__display__ = "HeaderTag"
FooterTag.__display__ = "HeaderTag"
AsideTag.__display__  = "AsideTag"

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
