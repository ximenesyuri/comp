

def _render(component: COMPONENT, **vars) -> Str:
    """
    Renders the given component, passing keyword argument variables.
    Handles Inner defaults, model coercion, context construction,
    supports depends_on, and dependency injection as in the legacy version.
    """
    try:
        definer = getattr(component, "func", component)
        context = dict(vars)
        sig = signature(definer)
        params = list(sig.parameters.values())
        depends_on = []
        if 'depends_on' in sig.parameters:
            depends_on_default = sig.parameters['depends_on'].default
            depends_on = context.pop('depends_on', depends_on_default) or []
        if depends_on is None:
            depends_on = []
        if not isinstance(depends_on, (list, tuple, set)):
            raise TypeError("depends_on must be a list, tuple, or set.")

        call_args = {}
        for param in params:
            if param.name == "depends_on":
                continue
            if param.name in context:
                val = context[param.name]
                if (hasattr(param.annotation, '__name__')
                        and (param.annotation.__name__.startswith("Model") or param.annotation.__name__.endswith("MODEL"))):
                    from typed.models import MODEL
                    ann = param.annotation
                    if (not isinstance(val, ann)) and isinstance(val, dict):
                        val = ann(val)
                call_args[param.name] = val
            elif param.default is not param.empty:
                call_args[param.name] = param.default
            elif getattr(param.annotation, '__name__', '') == 'Inner':
                call_args[param.name] = ''
            else:
                raise TypeError(f"Missing required argument '{param.name}' for component '{definer.__name__}'")

        if 'depends_on' in sig.parameters:
            result = definer(**call_args, depends_on=depends_on)
        else:
            result = definer(**call_args)

        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], str) and isinstance(result[1], dict):
            jinja_block_string, comp_locals = result
        else:
            jinja_block_string, comp_locals = result, {}

        from app.mods.helper.helper import _jinja_regex
        regex_str = re.compile(_jinja_regex(), re.DOTALL)
        match = regex_str.match(jinja_block_string)
        if not match:
            raise TypeError("Invalid Jinja block string format.")
        jinja_content = match.group(1)
        template_name = getattr(definer, '__name__', 'template')

        def make_rendered_dep_func(dep):
            def _inner(*args, **kwargs):
                from inspect import signature
                sig2 = signature(dep)
                param_names = [p.name for p in sig2.parameters.values()]
                child_context = dict(context)
                for i, value in enumerate(args):
                    if i < len(param_names):
                        child_context[param_names[i]] = value
                child_context.update(kwargs)
                dep_args = {}
                for p in sig2.parameters.values():
                    if p.name in child_context:
                        dep_args[p.name] = child_context[p.name]
                    elif p.default is not Parameter.empty:
                        dep_args[p.name] = p.default
                dep_block = dep(**dep_args)
                dep_match = re.compile(_jinja_regex(), re.DOTALL).match(dep_block)
                if not dep_match:
                    raise TypeError(f"Invalid Jinja block string format in dependency {dep.__name__}")
                dep_jinja_content = dep_match.group(1)
                from jinja2 import Environment, StrictUndefined
                env2 = Environment(undefined=StrictUndefined)
                dep_template = env2.from_string(dep_jinja_content)
                return dep_template.render(**child_context)
            return _inner

        full_jinja_context = dict(comp_locals)
        full_jinja_context.update(call_args)
        full_jinja_context.update(vars)

        for dep in depends_on:
            if not callable(dep):
                raise TypeError(f"Dependency {repr(dep)} is not a definer (function)")
            dep_name = getattr(dep, '__name__', str(dep))
            full_jinja_context[dep_name] = make_rendered_dep_func(dep)

        from jinja2 import Environment, DictLoader, StrictUndefined
        env = Environment(
            loader=DictLoader({template_name: jinja_content}),
            undefined=StrictUndefined
        )
        template = env.get_template(template_name)
        return template.render(**full_jinja_context)
    except Exception as e:
        from app.mods.err import RenderErr
        raise RenderErr(e)
