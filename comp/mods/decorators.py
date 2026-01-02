import re
from inspect import signature, Parameter
from functools import wraps, update_wrapper
from typed import TYPE, name, typed, Dict, Lazy, Typed, Any, Union, Str
from comp.mods.helper.types_ import COMP
from comp.mods.helper.helper import _jinja, _jinja_env
from comp.mods.types.base import Jinja, LAZY_COMP

@typed
def jinja(arg: Union(Typed(Any, cod=Str), Lazy, Str)) -> Jinja:
    if arg in Str:
        return _jinja(arg)
    else:
        if arg.codomain <= Jinja:
            return arg


def comp(arg=None, *, lazy=True):
    def _build_comp(func):
        from typed import Function
        if not func in Function:
            raise TypeError(
                "Comp decorator can only be applied to function objects:\n"
                f" ==> '{name(func)}': has wrong type\n"
                f"     [expected_type] Function\n"
                f"     [received_type] {name(TYPE(func))}"
            )

        original_sig = signature(func)
        func.__signature__ = original_sig

        sig = signature(func)
        if "__context__" in sig.parameters:
            param = sig.parameters["__context__"]
            expected_type_hint = Dict
            if param.annotation is Parameter.empty:
                func.__annotations__["__context__"] = expected_type_hint
            else:
                if not (param.annotation <= Dict):
                    raise TypeError(
                        "In a comp, argument '__context__' must be of type Dict.\n"
                        f" ==> '{name(func)}': has '__context__' of wrong type\n"
                        f"     [received_type]: '{name(param.annotation)}'"
                    )

        typed_arg = typed(func, lazy=False)
        typed_arg.__class__ = COMP

        if not typed_arg.codomain <= Jinja:
            raise TypeError(
                "A comp should create a Jinja string:\n"
                f" ==> '{name(func)}' codomain is not a subclass of Jinja\n"
                f"     [received_type]: '{name(typed_arg.codomain)}'"
            )

        func_sig = signature(func)

        @wraps(func)
        def comp_wrapper(*args, **kwargs):
            if '__context__' in func_sig.parameters:
                param_names = list(func_sig.parameters)
                context_index = param_names.index('__context__')
                if len(args) <= context_index and '__context__' not in kwargs:
                    kwargs['__context__'] = {}

            jinja_str = func(*args, **kwargs)

            bound = func_sig.bind(*args, **kwargs)
            bound.apply_defaults()
            context = dict(bound.arguments)
            if '__context__' in context and context['__context__']:
                context.update(context['__context__'])

            jinja_src = re.sub(r"^jinja\s*\n?", "", jinja_str)
            template = _jinja_env().from_string(jinja_src)
            rendered = template.render(**context)
            return _jinja(rendered)

        typed_wrapper = typed(comp_wrapper, lazy=False)
        typed_wrapper.__class__ = COMP
        return typed_wrapper

    def _make_lazy_wrapper(func):
        class LazyComp(Lazy):
            is_lazy = True

            def __init__(self, f):
                self._orig = f
                self._wrapped = None
                self.func = f
                self.lazy = True

                update_wrapper(self, f)

            def _materialize(self):
                if self._wrapped is None:
                    self._wrapped = _build_comp(self._orig)
                return self._wrapped

            def __call__(self, *a, **kw):
                return self._materialize()(*a, **kw)

            def __getattr__(self, name_):
                return getattr(self._materialize(), name_)

            def __repr__(self):
                return f"<LazyComp for {getattr(self._orig, '__name__', 'anonymous')}>"

        inst = type.__call__(LazyComp, func)
        return inst

    def decorator(func):
        if not lazy:
            return _build_comp(func)
        return _make_lazy_wrapper(func)

    if arg is None:
        return decorator
    else:
        return decorator(arg)
