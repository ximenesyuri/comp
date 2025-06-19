import functools
from typed import typed, nill, TypedFuncType, Callable
from jinja2 import Environment, DictLoader, StrictUndefined
from app.mods.types import JinjaStr
from app.err import ComponentErr

def component(definer):
    try:
        typed_definer = typed(definer)

        if typed_definer.codomain is not JinjaStr:
            raise TypeError(
                f"Function '{template_function.__name__}' decorated with @component "
                "must have a codomain (return type hint) of JinjaStr. "
                f"Found: {getattr(typed_function.codomain, '__name__', str(typed_function.codomain))}"
            )

        @functools.wraps(definer)
        def component_wrapper(*args, **kwargs):
            template_string = typed_definer.func(*args, **kwargs)

            if not isinstance(template_string, JinjaStr):
                warnings.warn(
                    f"Unexpected: Typed function '{typed_definer.__name__}' returned "
                    f"a non-JinjaStr value despite its type hint. Received type: {type(template_string).__name__}.", RuntimeWarning
                )
                raise TypeError(
                    f"Function {typed_definer.__name__} decorated with @component "
                    "did not return a valid Jinja template string as expected."
                )

            template_name = typed_definer.__name__
            env = Environment(
                loader=DictLoader({template_name: template_string}),
                undefined=StrictUndefined
                )
            template = env.get_template(template_name)

            return template.render(*args, **kwargs)

        component_wrapper.__is_component__ = True

        return component_wrapper
    except Exception as e:
        raise ComponentErr(e)
