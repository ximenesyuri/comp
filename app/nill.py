from app.mods.helper import (
    _nill_jinja,
    _nill_component,
    _nill_static,
    _nill_definer,
    _get_variables_map
)

# ---------------------------
#       NILL INSTANCES
# --------------------------- 
nill_jinja   = _nill_jinja
nill_definer = _nill_definer()
nill_comp    = _nill_component()
nill_static  = _nill_static
nill_head    = _nill_component('head')
nill_body    = _nill_component('body')
nill_header  = _nill_component('header')
nill_footer  = _nill_component('footer')
nill_aside   = _nill_component('aside')
