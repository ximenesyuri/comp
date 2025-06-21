from typed import Str, TypedFuncType
from app.mods.meta import _JinjaStr, _Component
from app.mods.factories import TagStr, Tag

# content string types
JinjaStr  = _JinjaStr('JinjaStr', (Str,), {})
HeaderStr = TagStr('header')
FooterStr = TagStr('footer')
LeftSidebarStr  = TagStr('left-sidebar')
RightSidebarStr = TagStr('right-sidebar')

# component types
Component = _Component('Component', (TypedFuncType,), {})
Header = Tag('header')

JinjaStr.__display__  = "JinjaStr"
HeaderStr.__display__ = "HeaderStr"
Component.__display__ = "Component"
