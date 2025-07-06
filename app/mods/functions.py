import re
from typed import typed, Str, List, Tuple, Dict, Any
from typed.models import MODEL
from inspect import signature, Signature, Parameter, getmodule
from jinja2 import meta, Environment, DictLoader, StrictUndefined
from app.mods.helper import _jinja_regex, _get_variables_map, _find_jinja_vars, _make_placeholder_model
from app.mods.definer import _definer
from app.mods.factories import Free
from app.mods.types import Definer, Jinja

@typed
def concat(definer1: Free(1), definer2: Definer) -> Definer:
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
        annotation = param.annotation if param.annotation != Parameter.empty else str
        if param.default != Parameter.empty:
            default_val = param.default
        elif isinstance(annotation, type) and isinstance(annotation, MODEL):
            default_val = _make_placeholder_model(n, annotation)
        else:
            default_val = ""
        new_parameters.append(Parameter(n, Parameter.KEYWORD_ONLY, default=default_val)) 

    for name in sorted(missing_vars):
        new_parameters.append(Parameter(name, Parameter.KEYWORD_ONLY, default=""))

    new_sig = Signature(new_parameters)
    def dynamic_definer(**kwargs):
        context = dict(kwargs)
        for param in new_parameters:
            if param.name not in context:
                ann = all_params[param.name].annotation if param.name in all_params and all_params[param.name].annotation != Parameter.empty else str
                context[param.name] = _make_placeholder_model(param.name, ann)
        return "jinja\n" + Environment(undefined=StrictUndefined).from_string(raw_jinja).render(**context)

    dynamic_definer.__signature__ = new_sig
    dynamic_definer.__annotations__ = {p.name: (all_params[p.name].annotation
                                               if p.name in all_params and all_params[p.name].annotation != Parameter.empty
                                               else str)
                                       for p in new_parameters}
    from app.mods.types import Jinja
    dynamic_definer.__annotations__['return'] = Jinja

    dyn_typed = typed(dynamic_definer)
    dyn_typed.__class__ = Definer
    dyn_typed._raw_combined_jinja = raw_jinja
    dyn_typed._is_dynamic_definer = True

    return dyn_typed

def join(*definers):
    if not definers:
        # Return an "empty" definer if nothing is joined!
        @typed
        def empty_join() -> str:
            return "jinja\n"
        empty_join.__class__ = Definer
        empty_join._is_dynamic_definer = True
        empty_join._raw_combined_jinja = ""
        return empty_join

    # 1. Combine raw Jinja blocks in order (static, i.e., not rendered now!)
    accumulated_raw_jinja_content = ""
    for d in definers:
        accumulated_raw_jinja_content += d.jinja

    # 2. Gather all unique arguments and types from all definers' signatures
    all_params = {}
    for d in definers:
        sig = signature(d)
        for n, p in sig.parameters.items():
            if n == "depends_on":  # Skip generic depends for now
                continue
            if n not in all_params:
                all_params[n] = p  # Use first occurrence

    # 3. Add all free Jinja variables as well (in case they're not covered as function parameters)
    env = Environment()
    ast = env.parse(accumulated_raw_jinja_content)
    all_jinja_vars = set(meta.find_undeclared_variables(ast))
    all_jinja_vars.discard("depends_on")
    param_names = set(all_params)
    missing_vars = all_jinja_vars - param_names

    # 4. Build the signature!
    new_parameters = []
    for n, p in all_params.items():
        annotation = p.annotation if p.annotation != Parameter.empty else str
        if p.default != Parameter.empty:
            default_val = p.default
        elif isinstance(annotation, type) and issubclass(annotation, MODEL):
            default_val = _make_placeholder_model(n, annotation)
        else:
            default_val = ""
        new_parameters.append(Parameter(n, Parameter.KEYWORD_ONLY, default=default_val))
    # Add any missing Jinja-only variables as string kwonly params (default "")
    for name in sorted(missing_vars):
        new_parameters.append(Parameter(name, Parameter.KEYWORD_ONLY, default=""))

    new_sig = Signature(new_parameters)
    # Prepare annotation dict for introspection
    annotations = {p.name: (all_params[p.name].annotation
                            if p.name in all_params and all_params[p.name].annotation != Parameter.empty
                            else str)
                   for p in new_parameters}
    from app.mods.types import Jinja
    annotations['return'] = Jinja

    def dynamic_joined_definer(**kwargs):
        context = dict(kwargs)
        # Fill in any missing params with placeholder models/defaults
        for param in new_parameters:
            if param.name not in context:
                ann = all_params[param.name].annotation if param.name in all_params and all_params[param.name].annotation != Parameter.empty else str
                context[param.name] = _make_placeholder_model(param.name, ann)
        # Render the combined jinja
        return "jinja\n" + Environment(undefined=StrictUndefined).from_string(accumulated_raw_jinja_content).render(**context)

    dynamic_joined_definer.__signature__ = new_sig
    dynamic_joined_definer.__annotations__ = annotations

    dyn_typed = typed(dynamic_joined_definer)
    dyn_typed.__class__ = Definer
    dyn_typed._is_dynamic_definer = True
    dyn_typed._raw_combined_jinja = accumulated_raw_jinja_content
    return dyn_typed
