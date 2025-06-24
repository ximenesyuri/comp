import re
from typed import typed, Str, TypedFuncType, Any, List, Json, Bool, Filter
from typed.models import Model, Optional
from app.mods.meta import _JinjaStr, _Definer, _Markdown
from app.mods.factories import TagStr, TagDefiner, Tag
from app.mods.helper import (
    _nill_jinja,
    _nill_component,
    _nill_static,
    _nill_definer,
    _collect_definer_variables_map
)

# ---------------------------
#    CONTENT STRING TYPES
# ---------------------------
JinjaStr  = _JinjaStr('JinjaStr', (Str,), {})
HeadStr   = TagStr('head')
BodyStr   = TagStr('body')
HeaderStr = TagStr('header')
FooterStr = TagStr('footer')
AsideStr  = TagStr('aside')
Markdown  = _JinjaStr('Markdown', (Str,), {})

JinjaStr.__display__  = "JinjaStr"
HeadStr.__display__   = "HeadStr"
BodyStr.__display__   = "BodyStr"
HeaderStr.__display__ = "HeaderStr"
FooterStr.__display__ = "HeaderStr"
AsideStr.__display__  = "AsideStr"
Markdown.__display__  = "Markdown"

# ---------------------------
#       DEFINER TYPES
# ---------------------------
Definer       = _Definer('Definer', (TypedFuncType,), {})
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
_Component = Model(
    definer=Definer,
    context=Json
)

_Static = Model(
    __extends__=Component,
    marker=Optional(Str, "content"),
    content=Markdown
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

@typed
def _check_static_context(static: _Static) -> Bool:
    definer = static.get('definer', _nill_definer())
    marker = static.get('marker', 'content')
    context = static.get('context', {})

    params = set(inspect.signature(definer).parameters)
    if marker in params:
        return False

    if marker in context:
        return False

    kwargs = {k: context[k] for k in params if k in context}
    try:
        jinja_str = definer(**kwargs)
    except Exception:
        return False

    pattern = r"\{\{\s*" + re.escape(marker) + r"\s*\}\}"
    found = re.search(pattern, jinja_str) is not None
    return found

Component = Filter(_Component, _check_context)
Static    = Filter(_Static, _check_static_context)
Head      = Tag('head')
Body      = Tag('body')
Header    = Tag('header')
Footer    = Tag('footer')
Aside     = Tag('left-sidebar')

Component.__display__ = "Component"
Static.__display__    = "Static"
Head.__display__      = "Head"
Body.__display__      = "Body"
Nav.__display__       = "Nav"
Header.__display__    = "Header"
Footer.__display__    = "Footer"
Aside.__display__     = "Aside"

# ---------------------------
#       NILL COMPONENTS
# --------------------------- 
nill_comp   = _nill_component()
nill_static = _nill_static
nill_head   = _nill_component('head')
nill_body   = _nill_component('body')
nill_nav    = _nill_component('nav')
nill_header = _nill_component('header')
nill_footer = _nill_component('footer')
nill_aside  = _nill_component('aside')
