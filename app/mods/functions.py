import re
from typed import typed, Str, List, Tuple, Dict, Any
from typed.models import MODEL
from inspect import signature, Signature, Parameter, getmodule
from jinja2 import meta, Environment, DictLoader, StrictUndefined
from app.mods.helper.helper import (
    _jinja_regex,
    _get_variables_map,
    _find_jinja_vars,
    _make_placeholder_model,
    _get_annotation
)
from app.mods.decorators.definer import definer
from app.mods.factories.base import Definer
from app.mods.types.base import Jinja, DEFINER

@typed
def concat(definer1: Definer(1), definer2: DEFINER) -> DEFINER:
    from inspect import Parameter, Signature

    outer_jinja = definer1.jinja
    inner_jinja = definer2.jinja

    slot_vars = set(definer1.jinja_free_vars)
    if len(slot_vars) != 1:
        raise ValueError(
            f"Concat requires exactly one free variable as slot in the outer definer. Found: {slot_vars}"
        )
    slot_var = list(slot_vars)[0]

    raw_jinja = outer_jinja.replace(f"{{{{{slot_var}}}}}", inner_jinja)

    sig1 = signature(definer1)
    sig2 = signature(definer2)
    params1 = {k: v for k, v in sig1.parameters.items() if k != slot_var and k != 'depends_on'}
    params2 = {k: v for k, v in sig2.parameters.items() if k != 'depends_on'}
    all_params = {**params2, **params1}

    from jinja2 import Environment, meta, StrictUndefined
    env = Environment()
    ast = env.parse(raw_jinja)
    jinja_vars = set(meta.find_undeclared_variables(ast))
    jinja_vars.discard(slot_var)
    jinja_vars.discard('depends_on')

    all_names = set(all_params)
    missing_vars = jinja_vars - all_names

    new_parameters = []
    for n in all_params:
        param = all_params[n]
        annotation = _get_annotation(param)
        if param.default != Parameter.empty:
            default_val = param.default
        elif isinstance(annotation, type) and issubclass(annotation, MODEL):
            default_val = _make_placeholder_model(n, annotation)
        else:
            default_val = ""
        new_parameters.append(Parameter(n, Parameter.KEYWORD_ONLY, default=default_val, annotation=annotation))
    for name in sorted(missing_vars):
        new_parameters.append(Parameter(name, Parameter.KEYWORD_ONLY, default="", annotation=str))

    new_sig = Signature(new_parameters)

    def dynamic_definer(**kwargs):
        context = dict(kwargs)
        for param in new_parameters:
            if param.name not in context:
                ann = param.annotation if hasattr(param, 'annotation') else str
                context[param.name] = _make_placeholder_model(param.name, ann)
        return "jinja\n" + Environment(undefined=StrictUndefined).from_string(raw_jinja).render(**context)

    dynamic_definer.__signature__ = new_sig
    dynamic_definer.__annotations__ = {p.name: p.annotation if hasattr(p, 'annotation') else str for p in new_parameters}
    from app.mods.types import Jinja
    dynamic_definer.__annotations__['return'] = Jinja

    dyn_typed = typed(dynamic_definer)
    dyn_typed.__class__ = DEFINER
    dyn_typed._raw_combined_jinja = raw_jinja
    dyn_typed._is_dynamic_definer = True
    return dyn_typed

@typed
def join(*definers: Tuple(DEFINER)) -> DEFINER:
    from typed.models import MODEL
    from inspect import Parameter, Signature

    if not definers:
        @typed
        def empty_join() -> str:
            return "jinja\n"
        empty_join.__class__ = DEFINER
        empty_join._is_dynamic_definer = True
        empty_join._raw_combined_jinja = ""
        return empty_join

    accumulated_raw_jinja_content = ""
    for d in definers:
        accumulated_raw_jinja_content += d.jinja

    all_params = {}
    for d in definers:
        sig = signature(d)
        for n, p in sig.parameters.items():
            if n == "depends_on":
                continue
            if n not in all_params:
                all_params[n] = p

    from jinja2 import Environment, meta, StrictUndefined
    env = Environment()
    ast = env.parse(accumulated_raw_jinja_content)
    all_jinja_vars = set(meta.find_undeclared_variables(ast))
    all_jinja_vars.discard("depends_on")
    param_names = set(all_params)
    missing_vars = all_jinja_vars - param_names

    new_parameters = []
    for n, p in all_params.items():
        annotation = _get_annotation(p)
        if p.default != Parameter.empty:
            default_val = p.default
        elif isinstance(annotation, type) and issubclass(annotation, MODEL):
            default_val = _make_placeholder_model(n, annotation)
        else:
            default_val = ""
        new_parameters.append(Parameter(n, Parameter.KEYWORD_ONLY, default=default_val, annotation=annotation))
    for name in sorted(missing_vars):
        new_parameters.append(Parameter(name, Parameter.KEYWORD_ONLY, default="", annotation=str))

    new_sig = Signature(new_parameters)
    __annotations__ = {p.name: p.annotation if hasattr(p, 'annotation') else str for p in new_parameters}
    from app.mods.types import Jinja
    __annotations__['return'] = Jinja

    def dynamic_joined_definer(**kwargs):
        context = dict(kwargs)
        for param in new_parameters:
            if param.name not in context:
                ann = param.annotation if hasattr(param, 'annotation') else str
                context[param.name] = _make_placeholder_model(param.name, ann)
        return "jinja\n" + Environment(undefined=StrictUndefined).from_string(accumulated_raw_jinja_content).render(**context)

    dynamic_joined_definer.__signature__ = new_sig
    dynamic_joined_definer.__annotations__ = __annotations__

    dyn_typed = typed(dynamic_joined_definer)
    dyn_typed.__class__ = DEFINER
    dyn_typed._is_dynamic_definer = True
    dyn_typed._raw_combined_jinja = accumulated_raw_jinja_content
    return dyn_typed
