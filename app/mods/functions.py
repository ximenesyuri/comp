import re
from inspect import signature, Parameter, Signature, _empty
from typed import typed, Tuple, Dict, Any, Str
from app.mods.decorators.base import component
from app.mods.types.base import Jinja, COMPONENT, Inner
from app.err import ConcatErr, JoinErr, EvalErr
from app.mods.helper.functions import _merge_context, _get_context, _copy
from app.mods.helper.helper import _get_jinja

@typed
def copy(comp: COMPONENT, **renamed_args: Dict(Str)) -> COMPONENT:
    return component(_copy(comp, **renamed_args))

@typed
def concat(comp_1: COMPONENT(1), comp_2: COMPONENT) -> COMPONENT:
    try:
        sig1 = signature(comp_1)
        sig2 = signature(comp_2)
        inner_param_name = None
        for name, param in sig1.parameters.items():
            if param.annotation is Inner:
                inner_param_name = name
                break
        if inner_param_name is None:
            raise ValueError(f"comp_1 must have a parameter with type annotation '{Inner.__name__}'")

        merged_params = []
        param_names = set()
        for p in sig1.parameters.values():
            if p.name == inner_param_name:
                continue
            merged_params.append(p)
            param_names.add(p.name)
        for p in sig2.parameters.values():
            if p.name not in param_names and p.name != '__context__':
                merged_params.append(p)
                param_names.add(p.name)

        merged_ctx = _merge_context(comp_1, comp_2)
        merged_params.append(Parameter('__context__', kind=Parameter.KEYWORD_ONLY, default=merged_ctx, annotation=Dict(Any)))
        new_sig = Signature(parameters=merged_params, return_annotation=Jinja)
        new_annotations = {k: v.annotation for k, v in [(p.name, p) for p in merged_params]}
        new_annotations['return'] = Jinja

        def wrapper(*args, **kwargs):
            ba = new_sig.bind(*args, **kwargs)
            ba.apply_defaults()
            context = dict(merged_ctx)
            user_ctx = ba.arguments.get('__context__', {})
            context.update(user_ctx)

            # Call comp_2 first to supply "inner" result into comp_1 at the right param.
            c2_args = {p.name: ba.arguments[p.name] for p in sig2.parameters.values() if p.name in ba.arguments and p.name != '__context__'}
            if '__context__' in sig2.parameters:
                c2_args['__context__'] = context
            inner_result = comp_2(**c2_args)

            c1_args = {p.name: ba.arguments[p.name] for p in sig1.parameters.values() if p.name in ba.arguments and p.name != inner_param_name and p.name != '__context__'}
            c1_args[inner_param_name] = inner_result
            if '__context__' in sig1.parameters:
                c1_args['__context__'] = context
            return comp_1(**c1_args)

        wrapper.__signature__ = new_sig
        wrapper.__annotations__ = dict(new_annotations)
        comp = component(wrapper)
        jinja1 = _get_jinja(comp_1)
        jinja2 = _get_jinja(comp_2)
        concat_jinja = jinja1
        concat_jinja = re.sub(r"^jinja\s*\n?", "", concat_jinja)
        concat_jinja = re.sub(r'{\s*' + re.escape(inner_param_name) + r'\s*}', jinja2, concat_jinja)
        concat_jinja = re.sub(r'\[\[\s*' + re.escape(inner_param_name) + r'\s*\]\]', jinja2, concat_jinja)
        comp._jinja = concat_jinja
        return comp
    except Exception as e:
        raise ConcatErr(e)

@typed
def join(*comps: Tuple(COMPONENT)) -> COMPONENT:
    try:
        if not comps:
            raise ValueError("At least one component must be provided")
        sigs = [signature(comp) for comp in comps]
        param_names = set()
        merged_params = []
        for sig in sigs:
            for p in sig.parameters.values():
                if p.name not in param_names and p.name != '__context__':
                    merged_params.append(p)
                    param_names.add(p.name)
        merged_ctx = _merge_context(*comps)
        merged_params.append(Parameter('__context__', kind=Parameter.KEYWORD_ONLY, default=merged_ctx, annotation=Dict(Any)))
        new_sig = Signature(parameters=merged_params, return_annotation=Jinja)
        new_annotations = {k: v.annotation for k, v in [(p.name, p) for p in merged_params]}
        new_annotations['return'] = Jinja

        def wrapper(*args, **kwargs):
            ba = new_sig.bind(*args, **kwargs)
            ba.apply_defaults()
            context = dict(merged_ctx)
            user_ctx = ba.arguments.get('__context__', {})
            context.update(user_ctx)
            results = []
            for comp, sig in zip(comps, sigs):
                local_args = {p.name: ba.arguments[p.name] for p in sig.parameters.values() if p.name in ba.arguments and p.name != '__context__'}
                if '__context__' in sig.parameters:
                    local_args['__context__'] = context
                results.append(comp(**local_args))
            return Jinja(''.join(str(r) for r in results))
        wrapper.__signature__ = new_sig
        wrapper.__annotations__ = dict(new_annotations)
        comp = component(wrapper)

        joined_jinja_list = [_get_jinja(c) for c in comps]
        for i in range(len(joined_jinja_list)):
            joined_jinja_list[i] = re.sub(r"^jinja\s*\n?", "", joined_jinja_list[i])
        joined_jinja = "".join(joined_jinja_list)
        comp._jinja = joined_jinja

        return comp
    except Exception as e:
        raise JoinErr(e)

@typed
def eval(func: COMPONENT, **fixed_kwargs: Dict(Any)) -> COMPONENT:
    try:
        sig = signature(func)
        old_params = list(sig.parameters.items())

        context_in_sig = '__context__' in sig.parameters
        merged_ctx = _get_context(func)

        new_params = []
        for name, param in old_params:
            if name in fixed_kwargs:
                new_params.append(Parameter(name, kind=param.kind, default=fixed_kwargs[name], annotation=param.annotation))
            elif name == '__context__':
                new_params.append(Parameter('__context__', kind=Parameter.KEYWORD_ONLY, default=merged_ctx, annotation=Dict(Any)))
            else:
                new_params.append(param)
        if not context_in_sig:
            new_params.append(Parameter('__context__', kind=Parameter.KEYWORD_ONLY, default=merged_ctx, annotation=Dict(Any)))
        new_sig = Signature(new_params)

        def wrapper(*args, **kwargs):
            if __context__ is None:
                __context__ = dict(merged_ctx)
            ba = new_sig.bind_partial(*args, **kwargs)
            ba.apply_defaults()
            context = dict(merged_ctx)
            user_ctx = ba.arguments.get('__context__', {})
            context.update(user_ctx)
            call_kwargs = dict(fixed_kwargs)
            call_kwargs.update({k: v for k, v in ba.arguments.items() if k != '__context__'})
            call_kwargs['__context__'] = context

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
        wrapper.__annotations__["__context__"] = Dict(Any)
        comp = component(wrapper)

        base_jinja = _get_jinja(func)
        base_jinja = re.sub(r'^jinja\s*\n?', '', base_jinja)
        jinja_eval = base_jinja
        for k, v in fixed_kwargs.items():
            jinja_eval = re.sub(r'\[\[\s*' + re.escape(k) + r'\s*\]\]', str(v), jinja_eval)
            jinja_eval = re.sub(r'{{\s*' + re.escape(k) + r'\s*}}', str(v), jinja_eval)
            jinja_eval = re.sub(r'{\s*' + re.escape(k) + r'\s*}', str(v), jinja_eval)
        comp._jinja = jinja_eval

        return comp
    except Exception as e:
        raise EvalErr(e)

