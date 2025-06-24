from typed import typed, Str, TypedFuncType, Any, List, Json, Bool, Filter
from typed.models import Model, Optional
from app.mods.meta import _JinjaStr, _Definer
from app.mods.factories import TagStr, TagDefiner, Tag
from app.mods.helper import (
    _nill_jinja,
    _nill_component,
    _collect_definer_variables_map
)

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

# component types
_Component = Model(
    definer=Definer,
    context=Optional(Json, {})
)

@typed
def _check_context(component: _Component) -> Bool:
    definer = component.get('definer')
    context = component.get('context', {})

    from inspect import signature
    depends_on = []
    sig = signature(getattr(definer, "func", definer))
    if 'depends_on' in sig.parameters:
        depends_on_default = sig.parameters['depends_on'].default
        depends_on = context.get('depends_on', depends_on_default) or []
    if depends_on is None:
        depends_on = []
    if not isinstance(depends_on, (list, tuple, set)):
        raise TypeError("depends_on must be list, tuple, or set.")

    context_keys = set(context)
    for dep in depends_on:
        if callable(dep):
            context_keys.add(getattr(dep, '__name__', str(dep)))

    variables_needed_map = _collect_definer_variables_map(definer)
    missing = [v for v in variables_needed_map if v not in context_keys]
    if not missing:
        return True
    messages = []
    for v in missing:
        trace = " -> ".join(variables_needed_map[v])
        messages.append(f"'{v}' (found in: {trace})")
    message = (
        "The following Jinja variables are not defined in the context:\n"
        + "\n".join(messages)
    )
    raise ValueError(message)

Component = Filter(_Component, _check_context)

Header       = Tag('header')
Footer       = Tag('footer')
LeftSidebar  = Tag('left-sidebar')
RightSidebar = Tag('right-sidebar')

Component.__display__    = "Component"
Header.__display__       = "Header"
Footer.__display__       = "Footer"
LeftSidebar.__display__  = "LeftSidebar"
RightSidebar.__display__ = "RightSidebar"


