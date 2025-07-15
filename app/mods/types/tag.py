from app.mods.factories.base import TAG

HEAD   = TAG('head')
BODY   = TAG('body')
HEADER = TAG('header')
FOOTER = TAG('footer')
ASIDE  = TAG('aside')

HEAD.__display__   = "HEAD"
BODY.__display__   = "BODY"
HEADER.__display__ = "HEADER"
FOOTER.__display__ = "FOOTER"
ASIDE.__display_   = "ASIDE"
