import functools
from inspect import signature
from typed import typed, nill, TypedFuncType, Callable
from jinja2 import Environment, DictLoader, StrictUndefined
from app.mods.types import JinjaStr
from app.err import ComponentErr
from app.vars import JINJA_BLOCK_REGEX

def component(definer=nill):
    """
    Decorator that applies @typed and wraps the function to render JinjaStr.
    Extracts the Jinja content from the special string block.
    """
    typed_function = typed(definer)

    if typed_function.codomain is not JinjaStr:
        raise TypeError(
            f"Function '{definer.__name__}' decorated with @component "
            "must have a codomain (return type hint) of JinjaStr. "
            f"Found: {getattr(typed_function.codomain, '__name__', str(typed_function.codomain))}"
        )

    @functools.wraps(definer)
    def __component(*args, **kwargs):
        template_block_string = typed_function.func(*args, **kwargs)

        if not isinstance(template_block_string, JinjaStr):
            raise TypeError("Invalid value returned by typed function.")

        match = JINJA_BLOCK_REGEX.match(template_block_string)
        if not match:
            raise TypeError("Invalid Jinja block string format.")

        jinja_content = match.group(1)

        template_name = typed_function.__name__
        env = Environment(
            loader=DictLoader({template_name: jinja_content}),
            undefined=StrictUndefined
        )
        template = env.get_template(template_name)

        sig = signature(definer)
        params = list(sig.parameters.values())
        bound_args = {}
        for i, arg in enumerate(args):
            if i < len(params):
                pname = params[i].name
                bound_args[pname] = arg
        bound_args.update(kwargs)
        return template.render(**bound_args)

    __component.__is_component__ = True

    return __component
