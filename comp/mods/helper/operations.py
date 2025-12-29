from inspect import signature, Signature, Parameter, _empty
from functools import wraps

def _order_params(params):
    po = []
    pk = []
    var_po = None
    ko = []
    var_ko = None
    for p in params:
        if p.kind == Parameter.POSITIONAL_ONLY:
            po.append(p)
        elif p.kind == Parameter.POSITIONAL_OR_KEYWORD:
            pk.append(p)
        elif p.kind == Parameter.VAR_POSITIONAL:
            var_po = p
        elif p.kind == Parameter.KEYWORD_ONLY:
            ko.append(p)
        elif p.kind == Parameter.VAR_KEYWORD:
            var_ko = p
    result = po + pk
    if var_po:
        result.append(var_po)
    result += ko
    if var_ko:
        result.append(var_ko)
    return result

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

def _copy(func, **rename_map):
    if not callable(func):
        raise TypeError("copy_function expects a callable as input")

    seen = set()
    while hasattr(func, '__wrapped__') and func not in seen:
        seen.add(func)
        func = func.__wrapped__

    from utils import func as func_
    func = func_.unwrap(func)
    old_sig = signature(func)
    new_params = []
    new_annotations = {}
    name_map = {}

    for param in old_sig.parameters.values():
        new_name = rename_map.get(param.name, param.name)
        name_map[new_name] = param.name
        new_param = Parameter(
            new_name,
            kind=param.kind,
            default=param.default,
            annotation=param.annotation
        )
        new_params.append(new_param)
        if param.annotation is not _empty:
            new_annotations[new_name] = param.annotation

    new_sig = Signature(parameters=new_params, return_annotation=old_sig.return_annotation)
    new_annotations['return'] = old_sig.return_annotation

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = new_sig.bind(*args, **kwargs)
        bound.apply_defaults()
        mapped_kwargs = { name_map[k]: v for k,v in bound.arguments.items() }
        return func(**mapped_kwargs)

    wrapper.__signature__ = new_sig
    wrapper.__annotations__ = new_annotations

    for attr in ('_jinja', ):
        if hasattr(func, attr):
            setattr(wrapper, attr, getattr(func, attr))

    return wrapper
