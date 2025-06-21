import functools
from inspect import signature
from typed import typed, nill, TypedFuncType, Callable
from jinja2 import Environment, DictLoader, StrictUndefined
from app.err import ComponentErr
from app.vars import JINJA_STR_REGEX

def component(definer=nill):
    """
    Decorator that applies @typed and wraps the function to render JinjaStr.
    Extracts the Jinja content from the special string block.
    Supports "depends_on" param: a list/tuple/set of components to be made available in the template.
    """
    from app.mods.types import JinjaStr, Component
    typed_function = typed(definer)

    if not issubclass(typed_function.codomain, JinjaStr):
        raise TypeError(
            f"Function '{definer.__name__}' decorated with @component "
            "must have a codomain (return type hint) of JinjaStr. "
            f"Found: {getattr(typed_function.codomain, '__name__', str(typed_function.codomain))}"
        )

    @functools.wraps(definer)
    def _component(*args, **kwargs):
        sig = signature(definer)
        # get default depends_on if not passed:
        if 'depends_on' in sig.parameters:
            depends_on_default = sig.parameters['depends_on'].default
            depends_on = kwargs.pop('depends_on', depends_on_default)
        else:
            depends_on = []

        # call the base function without depends_on in its signature
        params = list(sig.parameters.values())
        bound_args = {}
        param_names = [p.name for p in params]
        for i, arg in enumerate(args):
            if i < len(params):
                pname = param_names[i]
                bound_args[pname] = arg
        bound_args.update(kwargs)
        # Remove depends_on for the base function if present
        if 'depends_on' in bound_args:
            del bound_args['depends_on']

        template_block_string = typed_function.func(**bound_args)

        if not isinstance(template_block_string, JinjaStr):
            raise TypeError("Invalid value returned by typed function.")

        match = JINJA_STR_REGEX.match(template_block_string)
        if not match:
            raise TypeError("Invalid Jinja block string format.")

        jinja_content = match.group(1)
        template_name = typed_function.__name__
        env = Environment(
            loader=DictLoader({template_name: jinja_content}),
            undefined=StrictUndefined
        )
        template = env.get_template(template_name)

        # Validate & inject depends_on
        if depends_on is None:
            depends_on = []
        if not isinstance(depends_on, (list, tuple, set)):
            raise TypeError("depends_on must be a list, tuple, or set.")
        dep_context = {}
        for dep in depends_on:
            if not isinstance(dep, Component):
                raise TypeError(f"Dependency {dep} is not a valid component (not an instance of Component)!")
            dep_context[dep.__name__] = dep

        # Now, re-bind (for call signature correctness):
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()
        # Remove 'depends_on' if in the signature/binding
        bound.arguments.pop('depends_on', None)
        context = dict(bound.arguments)
        context.update(dep_context)

        return template.render(**context)

    _component.is_component = True

    return _component
