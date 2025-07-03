import inspect
from app.mods.functions import concat
from app.mods.factories import FreeDefiner
from app.mods.types import Definer
from app.mods.helper import _FREE_DEFINER_REGISTRY

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
