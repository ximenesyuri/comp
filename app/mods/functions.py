import re
from functools import wraps
from collections import defaultdict
from typed import typed, Str, List, Tuple, Dict, Any
from utils import func
from inspect import signature, Signature, Parameter, getmodule, _empty
from app.mods.decorators.base import component
from app.mods.types.base import Jinja, COMPONENT, Inner
from app.err import ConcatErr, JoinErr, EvalErr

@typed
def Component(comp: COMPONENT, **renamed_args: Dict(Str)) -> COMPONENT:
    return component(func.copy(comp, **renamed_args))

@typed
def concat(comp_1: COMPONENT(1), comp_2: COMPONENT) -> COMPONENT:
    try:
        sig1 = signature(comp_1)
        sig2 = signature(comp_2)

        inner_param_name: str | None = None
        inner_param_obj: Parameter | None = None
        for name, param in sig1.parameters.items():
            if param.annotation is Inner or (hasattr(param.annotation, '__origin__') and param.annotation.__origin__ is TypeVar and Inner in param.annotation.__args__):
                inner_param_name = name
                inner_param_obj = param
                break
        if inner_param_name is None:
            raise ValueError(f"comp_1 must have a parameter with type annotation '{Inner.__name__}'")

        params_for_new_sig_from_comp1 = [p for p in sig1.parameters.values() if p.name != inner_param_name]
        params_for_new_sig_from_comp2 = list(sig2.parameters.values())

        unique_params_dict: dict[str, Parameter] = {}
        new_annotations: dict[str, Any] = {}

        for p in params_for_new_sig_from_comp1:
            if p.name not in unique_params_dict:
                unique_params_dict[p.name] = p
                if p.annotation is not _empty:
                    new_annotations[p.name] = p.annotation

        for p in params_for_new_sig_from_comp2:
            if p.name not in unique_params_dict:
                unique_params_dict[p.name] = p
                if p.annotation is not _empty:
                    new_annotations[p.name] = p.annotation

        new_params = list(unique_params_dict.values())
        new_sig = Signature(parameters=new_params, return_annotation=Jinja)

        def wrapper(*args, **kwargs):
            ba = new_sig.bind(*args, **kwargs)
            ba.apply_defaults()

            c1_args = {}
            for p in sig1.parameters.values():
                if p.name == inner_param_name:
                    continue
                c1_args[p.name] = ba.arguments[p.name]

            c2_args = {}
            for p in sig2.parameters.values():
                c2_args[p.name] = ba.arguments[p.name]

            inner_value = comp_2(**c2_args)
            c1_args[inner_param_name] = inner_value
            return comp_1(**c1_args)

        wrapper.__signature__ = new_sig
        wrapper.__annotations__ = {name: anno for name, anno in new_annotations.items()}
        wrapper.__annotations__['return'] = Jinja

        return component(wrapper)
    except Exception as e:
        raise ConcatErr(e)

@typed
def join(*comps: Tuple(COMPONENT)) -> COMPONENT:
    try:
        if not comps:
            raise ValueError("At least one component must be provided")

        sigs = [signature(comp) for comp in comps]
        param_lists = [list(sig.parameters.values()) for sig in sigs]

        unique_params_dict = {}
        new_annotations = {}

        for params in param_lists:
            for p in params:
                if p.name not in unique_params_dict:
                    unique_params_dict[p.name] = p
                    if p.annotation is not _empty:
                        new_annotations[p.name] = p.annotation

        new_params = list(unique_params_dict.values())
        new_sig = Signature(parameters=new_params, return_annotation=Jinja)

        def wrapper(*args, **kwargs):
            ba = new_sig.bind(*args, **kwargs)
            ba.apply_defaults()
            results = []

            for i, comp in enumerate(comps):
                orig_sig = sigs[i]
                func_args = {}
                for orig_p in orig_sig.parameters.values():
                    func_args[orig_p.name] = ba.arguments[orig_p.name]
                results.append(comp(**func_args))

            return Jinja(''.join(str(r) for r in results))

        wrapper.__signature__ = new_sig

        wrapper.__annotations__ = {name: anno for name, anno in new_annotations.items()}
        wrapper.__annotations__['return'] = Jinja

        return component(wrapper)
    except Exception as e:
        raise JoinErr(e)

@typed
def eval(func: COMPONENT, **fixed_kwargs: Dict(Any)) -> COMPONENT:
    sig = signature(func)
    old_params = list(sig.parameters.items())
    missing = [k for k in fixed_kwargs if k not in sig.parameters]
    if missing:
        raise TypeError(
            f"{func.__name__} has no argument(s): {', '.join(missing)}"
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

    def wrapper(*args, **kwargs):
        ba = new_sig.bind_partial(*args, **kwargs)
        ba.apply_defaults()
        call_kwargs = dict(fixed_kwargs)
        call_kwargs.update(ba.arguments)
        template_str = func(**call_kwargs)

        if isinstance(template_str, str):
            from app.mods.helper.helper import _jinja_env
            env = _jinja_env()
            template = env.from_string(template_str)
            return template.render(**call_kwargs)
        else:
            return Jinja(template_str)

    wrapper.__signature__ = new_sig
    if hasattr(func, '__annotations__'):
        wrapper.__annotations__ = dict(func.__annotations__)

    return component(wrapper)
