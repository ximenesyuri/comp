def nill_comp():
    from comp.mods.types.base import Jinja
    from comp.mods.decorators import comp
    def _nill_comp() -> Jinja:
        return """jinja """
    return comp(_nill_comp, lazy=False)

def nill_lazy_comp():
    from comp.mods.types.base import Jinja
    from comp.mods.decorators import comp
    def _nill_lazy_comp() -> Jinja:
        return """jinja """
    return comp(_nill_lazy_comp, lazy=True)
