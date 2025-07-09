import re
from inspect import signature, getsource, Parameter
from functools import wraps
from typed import typed, List, TypedFuncType
from jinja2 import Environment, meta
from app.mods.meta import _Definer

_FREE_DEFINER_REGISTRY = {}

class Definer(_Definer('Definer', (TypedFuncType,), {})):
    @property
    def jinja(self):
        """
        Returns the Jinja string of the definer.
        For static definers, it parses the source.
        For dynamic definers created by `join` or `concat`, it returns the pre-combined raw Jinja template.
        """
        if hasattr(self, '_is_dynamic_definer') and self._is_dynamic_definer:
            if hasattr(self, '_raw_combined_jinja'):
                return self._raw_combined_jinja
            else:
                print(f"Warning: Dynamic definer {self.__name__} is missing _raw_combined_jinja attribute.")
                return ""
        else:
            code = getsource(self)
            regex_str = re.compile(r"\"\"\"jinja([\s\S]*?)\"\"\"", re.DOTALL)
            match = regex_str.search(code)
            if match:
                return match.group(1)
            return ""

    @property
    def args(self):
        return tuple(signature(self).parameters.keys())

    @property
    def jinja_vars(self):
        """
        Returns the tuple of all Jinja variables found in the definer's template.
        Uses _find_jinja_vars.
        """
        env = Environment()
        jinja_content = self.jinja
        if not jinja_content:
            return ()
        ast = env.parse(jinja_content)
        return tuple(sorted(meta.find_undeclared_variables(ast)))

    @property
    def jinja_free_vars(self):
        """Returns the tuple of free Jinja variables (not corresponding to arguments)."""
        all_vars = set(self.jinja_vars)
        arg_vars = set(self.args)
        arg_vars.discard("depends_on")
        return tuple(sorted(list(all_vars - arg_vars)))

    def __add__(self, other: 'Definer') -> 'Definer':
        """
        Implements definer_1 + definer_2 => join(definer_1, definer_2)
        """
        if not isinstance(other, Definer):
            return NotImplemented
        from app.mods.functions import join
        return join(self, other)

    def __mul__(self, other: 'Definer') -> 'Definer':
        """
        Implements definer_1 * definer_2 => concat(definer_1, definer_2)
        Here, definer_1 is assumed to be the 'free_definer' with a single free variable slot,
        and definer_2 is the content to fill that slot.
        """
        if not isinstance(other, Definer):
            return NotImplemented # Or raise TypeError
        InstanceFree = _FREE_DEFINER_REGISTRY.get('__FreeInstance__')
        if InstanceFree is None:
            from app.mods.factories import Free
            InstanceFree = Free(1)
            _FREE_DEFINER_REGISTRY['__FreeInstance__'] = InstanceFree

        if not isinstance(self, InstanceFree):
            raise TypeError(
                f"The left operand of '*' (i.e., '{self.__name__}') must be a Definer with "
                "exactly one free Jinja variable to be used with concat (Free(1)).\n"
                f"Its free variables are: {self.jinja_free_vars}"
            )

        from app.mods.functions import concat
        return concat(self, other)

def _definer(arg):
    """base decorator to create a definer"""
    if callable(arg):
        is_dynamic_wrapper = hasattr(arg, '_is_dynamic_definer') and \
                             getattr(arg, '_is_dynamic_definer') is True

        if not is_dynamic_wrapper:
            original_sig = signature(arg)
            arg.__signature__ = original_sig

        if "depends_on" in signature(arg).parameters:
            param = signature(arg).parameters["depends_on"]
            expected_type_hint = List(Definer)
            if param.annotation is Parameter.empty:
                if not is_dynamic_wrapper:
                    arg.__annotations__["depends_on"] = expected_type_hint
            else:
                if isclass(param.annotation) and issubclass(param.annotation, List) and \
                   hasattr(param.annotation, '__args__') and param.annotation.__args__ and \
                   issubclass(param.annotation.__args__[0], Definer):
                    pass
                else:
                    raise TypeError(
                        f"In a definer, argument 'depends_on' must be of type List(Definer).\n"
                        f" ==> '{arg.__name__}': has 'depends_on' of wrong type\n"
                        f"     [received_type]: '{param.annotation}'"
                    )
        typed_arg = typed(arg)
        typed_arg.__class__ = Definer
        from app.mods.types import Jinja
        if not issubclass(typed_arg.codomain, Jinja):
            raise TypeError(
                "A definer should create a Jinja string:\n"
                f" ==> '{arg.__name__}' codomain is not a subclass of Jinja\n"
                f"     [received_type]: '{typed_arg.codomain.__name__}'"
            )
        if is_dynamic_wrapper:
            if hasattr(arg, '_is_dynamic_definer'):
                typed_arg._is_dynamic_definer = arg._is_dynamic_definer
            if hasattr(arg, '_raw_combined_jinja'):
                typed_arg._raw_combined_jinja = arg._raw_combined_jinja
            if hasattr(arg, '_combined_params_dict'):
                typed_arg._combined_params_dict = arg._combined_params_dict
        res = wraps(arg)(typed_arg)
        _FREE_DEFINER_REGISTRY[arg.__name__] = res
        return res
    raise TypeError(
        "Definer decorator can only be applied to callable objects:\n"
        f" ==> '{arg.__name__}': is not callable\n"
        f"     [received_type] '{type(arg).__name__}'"
    )

class DefinerProxy:
    def __init__(self, default_decorator):
        self._deco = default_decorator

    def __call__(self, fn):
        return self._deco(fn)

    def __getattr__(self, free_name):
        def proxy(inner_fn):
            free_definer = _FREE_DEFINER_REGISTRY.get(free_name)
            if free_definer is None:
                raise NameError(
                    f"No definer named '{free_name}' registered in _FREE_DEFINER_REGISTRY "
                    f"(needed for '@definer.{free_name}')."
                )
            result_definer = self._deco(inner_fn)
            return concat(free_definer, result_definer)
        return proxy

definer = DefinerProxy(_definer)
