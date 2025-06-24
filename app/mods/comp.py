import re
import functools
from inspect import signature
from typed import typed, Union, Str
from jinja2 import Environment, DictLoader, StrictUndefined
from app.mods.helper import _jinja_regex
from app.err import ComponentErr
from app.mods.types import Component, JinjaStr, Static

@typed
def render(component: Component) -> Str:
    definer = component.get('definer')
    context = dict(component.get('context', {}))

    typed_function = getattr(definer, "func", definer)
    sig = signature(typed_function)
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
        if param.name == 'depends_on':
            continue
        if param.name in context:
            call_args[param.name] = context[param.name]
        elif param.default is param.empty:
            raise TypeError(f"Missing required parameter '{param.name}' for definer '{definer}'")
    template_block_string = definer(**call_args, depends_on=depends_on) if 'depends_on' in sig.parameters else definer(**call_args)
    if not isinstance(template_block_string, JinjaStr):
        raise TypeError("Invalid value returned by definer function (not JinjaStr).")

    regex_str = re.compile(_jinja_regex(), re.DOTALL)
    match = regex_str.match(template_block_string)
    if not match:
        raise TypeError("Invalid Jinja block string format.")
    jinja_content = match.group(1)
    template_name = getattr(definer, '__name__', 'template')

    dep_context = {}

    def make_rendered_dep_func(dep):
        def _inner(**values):
            child_context = dict(context)      # parent context
            child_context.update(values)
            dep_template_str = dep()
            dep_match = re.compile(_jinja_regex(), re.DOTALL).match(dep_template_str)
            if not dep_match:
                raise TypeError(f"Invalid Jinja block string format in dependency {dep.__name__}")
            dep_jinja_content = dep_match.group(1)
            env2 = Environment(undefined=StrictUndefined)
            dep_template = env2.from_string(dep_jinja_content)
            return dep_template.render(**child_context)
        return _inner

    for dep in depends_on:
        if not callable(dep):
            raise TypeError(f"Dependency {repr(dep)} is not a definer (function)")
        dep_name = getattr(dep, '__name__', str(dep))
        dep_context[dep_name] = make_rendered_dep_func(dep)

    jinja_context = {}
    jinja_context.update(dep_context)
    jinja_context.update(context)

    env = Environment(
        loader=DictLoader({template_name: jinja_content}),
        undefined=StrictUndefined
    )
    template = env.get_template(template_name)
    return template.render(**jinja_context)

@typed
def build(static_page: Static) -> Component:
    pass

