from inspect import signature, Parameter

def _get_context(func):
    sig = signature(getattr(func, "func", func))
    if "__context__" in sig.parameters:
        param = sig.parameters["__context__"]
        if param.default != Parameter.empty and isinstance(param.default, dict):
            return param.default.copy()
    return {}

def _merge_context(*comps):
    merged = {}
    for comp in comps:
        merged.update(_get_context(comp))
    return merged
