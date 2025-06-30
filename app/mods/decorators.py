from functools import wraps
from inspect import signature, Parameter
from typed import typed, List
from typing import get_origin
from app.mods.types import Jinja, Definer

def definer(arg):
    """Decorator that creates a definer"""
    if callable(arg):
        original_sig = signature(arg)
        if "depends_on" in original_sig.parameters:
            param = original_sig.parameters["depends_on"]
            expected_type_hint = List(Definer)
            if param.annotation is Parameter.empty:
                arg.__annotations__["depends_on"] = expected_type_hint
            else:
                if issubclass(arg.__annotations__["depends_on"], expected_type_hint):
                    pass
                else:
                    raise TypeError(
                        f"In a definer, argument 'depends_on' must be of type List(Definer).\n"
                        f" ==> '{arg.__name__}': has 'depends_on' of wrong type\n"
                        f"     [received_type]: '{param.annotation.__name__}'"
                    )
        typed_arg = typed(arg)
        if not issubclass(typed_arg.codomain, Jinja):
            raise TypeError(
                "A definer should create a Jinja string:\n"
                f" ==> '{arg.__name__}' codomain is not a subclass of Jinja\n"
                f"     [received_type]: '{typed_arg.codomain.__name__}'"
            )
        return wraps(arg)(typed_arg)
    raise TypeError(
        "Definer decorator can only be applied to callable objects:\n"
        f" ==> '{arg.__name__}': is not callable\n"
        f"     [received_type] '{type(arg).__name__}'"
    )
