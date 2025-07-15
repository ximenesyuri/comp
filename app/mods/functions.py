import re
from functools import wraps
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
from app.mods.decorators.component import component
from app.mods.factories.base import Component
from app.mods.types.base import Jinja, COMPONENT

@typed
def concat(component1: Component(1), component2: COMPONENT) -> COMPONENT:
    from inspect import Parameter, Signature

    outer_jinja = component1.jinja
    inner_jinja = component2.jinja

    slot_vars = set(component1.jinja_free_vars)
    if len(slot_vars) != 1:
        raise ValueError(
            f"Concat requires exactly one free variable as slot in the outer component. Found: {slot_vars}"
        )
    slot_var = list(slot_vars)[0]

    raw_jinja = outer_jinja.replace(f"{{{{{slot_var}}}}}", inner_jinja)

    sig1 = signature(component1)
    sig2 = signature(component2)
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

    def dynamic_component(**kwargs):
        context = dict(kwargs)
        for param in new_parameters:
            if param.name not in context:
                ann = param.annotation if hasattr(param, 'annotation') else str
                context[param.name] = _make_placeholder_model(param.name, ann)
        return "jinja\n" + Environment(undefined=StrictUndefined).from_string(raw_jinja).render(**context)

    dynamic_component.__signature__ = new_sig
    dynamic_component.__annotations__ = {p.name: p.annotation if hasattr(p, 'annotation') else str for p in new_parameters}
    from app.mods.types import Jinja
    dynamic_component.__annotations__['return'] = Jinja

    dyn_typed = typed(dynamic_component)
    dyn_typed.__class__ = COMPONENT
    dyn_typed._raw_combined_jinja = raw_jinja
    dyn_typed._is_dynamic_component = True
    return dyn_typed

@typed
def join(*components: Tuple(COMPONENT)) -> COMPONENT:
    from typed.models import MODEL
    from inspect import Parameter, Signature

    if not components:
        @typed
        def empty_join() -> str:
            return "jinja\n"
        empty_join.__class__ = COMPONENT
        empty_join._is_dynamic_component = True
        empty_join._raw_combined_jinja = ""
        return empty_join

    accumulated_raw_jinja_content = ""
    for d in components:
        accumulated_raw_jinja_content += d.jinja

    all_params = {}
    for d in components:
        sig = signature(d)
        for n, p in sig.parameters.items():
            if n == "depends_on":
                continue
            if n not in all_params:
                all_params[n] = p

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
        elif isinstance(annotation, type) and isinstance(annotation, MODEL):
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

    def dynamic_joined_component(**kwargs):
        context = dict(kwargs)
        for param in new_parameters:
            if param.name not in context:
                ann = param.annotation if hasattr(param, 'annotation') else str
                context[param.name] = _make_placeholder_model(param.name, ann)
        return "jinja\n" + Environment(undefined=StrictUndefined).from_string(accumulated_raw_jinja_content).render(**context)

    dynamic_joined_component.__signature__ = new_sig
    dynamic_joined_component.__annotations__ = __annotations__

    dyn_typed = typed(dynamic_joined_component)
    dyn_typed.__class__ = COMPONENT
    dyn_typed._is_dynamic_component = True
    dyn_typed._raw_combined_jinja = accumulated_raw_jinja_content
    return dyn_typed

@typed
def eval(some_component: COMPONENT, **fixed_kwargs: Dict(Any)) -> COMPONENT:
    sig = signature(some_component)
    old_params = list(sig.parameters.items())

    missing = [k for k in fixed_kwargs if k not in sig.parameters]
    if missing:
        raise TypeError(
            f"{some_component.__name__} has no argument(s): {', '.join(missing)}"
        )

    new_params = []
    for name, param in old_params:
        if name in fixed_kwargs:
            new_param = Parameter(
                name,
                kind=param.kind,
                default=fixed_kwargs[name],
                annotation=param.annotation
            )
            new_params.append(new_param)
        else:
            new_params.append(param)

    new_sig = Signature(new_params)

    def wrapped(*args, **kwargs):
        ba = new_sig.bind_partial(*args, **kwargs)
        ba.apply_defaults()
        result = some_component(**ba.arguments)
        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], str) and isinstance(result[1], dict):
            return result[0]
        return result

    wrapped.__signature__ = new_sig
    if hasattr(some_component, '__annotations__'):
        wrapped.__annotations__ = dict(some_component.__annotations__)

    wrapped_typed = typed(wrapped)
    from app.mods.helper.types import COMPONENT
    wrapped_typed.__class__ = COMPONENT
    wrapped_typed.func = wrapped
    return wrapped_typed
