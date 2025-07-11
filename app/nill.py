from app.mods.helper.types import (
    _nill_jinja,
    _nill_comp,
    _nill_static,
    _nill_definer,
)

# ---------------------------
#   NILL JINJA INSTANCES
# --------------------------- 
nill_jinja   = _nill_jinja
nill_definer = _nill_definer()
nill_comp    = _nill_comp()
nill_static  = _nill_static
nill_head    = _nill_comp('head')
nill_body    = _nill_comp('body')
nill_header  = _nill_comp('header')
nill_footer  = _nill_comp('footer')
nill_aside   = _nill_comp('aside')

# ---------------------------
#   NILL MODEL INSTANCES
# ---------------------------

