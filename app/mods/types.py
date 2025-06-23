from typed import typed, Str, TypedFuncType, Any, List, Json
from typed.models import Model, Optional
from app.mods.meta import _JinjaStr, _Definer
from app.mods.factories import TagStr, TagDefiner, Tag
from app.mods.helper import _nill_jinja, _nill_component

# content string types
JinjaStr        = _JinjaStr('JinjaStr', (Str,), {})
HeaderStr       = TagStr('header')
FooterStr       = TagStr('footer')
LeftSidebarStr  = TagStr('left-sidebar')
RightSidebarStr = TagStr('right-sidebar')

JinjaStr.__display__        = "JinjaStr"
HeaderStr.__display__       = "HeaderStr"
FooterStr.__display__       = "HeaderStr"
LeftSidebarStr.__display__  = "LeftSidebarStr"
RightSidebarStr.__display__ = "RightSidebarStr"

# definer types
Definer             = _Definer('Definer', (TypedFuncType,), {})
HeaderDefiner       = TagDefiner('header')
FooterDefiner       = TagDefiner('footer')
LeftSidebarDefiner  = TagDefiner('left-sidebar')
RightSidebarDefiner = TagDefiner('right-sidebar')

Definer.__display__            = "Definer"
HeaderDefiner.__display__      = "HeaderDefiner"
FooterDefiner.__display__      = "FooterDefiner"
LeftSidebarDefiner.__display_  = "LeftSidebarDefiner"
RightSidebarDefiner.__display_ = "RightSidebarDefiner"

# nill definers
nill_component     = _nill_component()
nill_header        = _nill_component('header')
nill_footer        = _nill_component('footer')
nill_left_sidebar  = _nill_component('left-sidebar')
nill_right_sidebar = _nill_component('right-sidebar')

# component types
Component = Model(
    definer=Definer,
    context=Optional(Json, {}),
    depends_on=Optional(List(Definer), [])
)
Header       = Tag('header')
Footer       = Tag('footer')
LeftSidebar  = Tag('left-sidebar')
RightSidebar = Tag('right-sidebar')

Component.__display__    = "Component"
Header.__display__       = "Header"
Footer.__display__       = "Footer"
LeftSidebar.__display__  = "LeftSidebar"
RightSidebar.__display__ = "RightSidebar"

PageStructure = Model(
    header=Optional(Header, nill_header),
    footer=Optional(Footer, nill_footer),
    left_sidebar=Optional(LeftSidebar, nill_left_sidebar),
    right_sidebar=Optional(RightSidebar, nill_right_sidebar)
)

Page = Model(
    definer=Definer,
    structure=Optional(PageStructure, {}),
    context=Optional(Json, {}),
)
