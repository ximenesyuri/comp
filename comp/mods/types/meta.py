import re
from typed import (
    TYPE,
    Str,
    Typed,
    names,
    MODEL,
    name
)

class JINJA(TYPE(Str)):
    def __instancecheck__(cls, instance):
        if not instance in Str:
            return False

        from comp.mods.helper.helper import _jinja_regex
        regex_str = re.compile(_jinja_regex(), re.DOTALL)
        match = regex_str.match(instance)
        if not match:
            return False
        jinja_content = match.group(1)
        try:
            from comp.mods.helper.helper import _jinja_env
            _jinja_env().parse(jinja_content)
            return True
        except Exception as e:
            print(f"{e}")
            return False

class INNER(TYPE(Str), TYPE(MODEL)):
    def __instancecheck__(cls, instance):
        if not instance in Str and not instance in MODEL:
            return False
        return True

class _COMPONENT(TYPE(Typed)):
    _param_cache = {}

    def __call__(self, *args, **kwargs):
        if len(args) == 3 \
           and isinstance(args[0], str) \
           and isinstance(args[1], tuple) \
           and isinstance(args[2], dict):
            return type.__call__(self, *args, **kwargs)

        from comp.mods.helper.types import COMPONENT as BASE
        from typed import name

        if self is BASE:
            types   = args
            cod     = kwargs.get('cod',     None)
            inner   = kwargs.get('inner',   None)
            content = kwargs.get('content', None)
            key     = (types, cod, inner, content)
            if key in self._param_cache:
                return self._param_cache[key]
            parts = []
            if types:
                parts.append(names(types))
            if cod is not None:
                parts.append(f"cod={name(cod)}")
            class_name = f"{name(BASE)}({", ".join(parts)})" if parts else name(BASE)

            attrs = {
                "__display__":    class_name,
                "_param_types":   types,
                "_param_cod":     cod,
                "_param_inner":   inner,
                "_param_content": content,
            }
            ParamComponent = self.__class__(class_name, (BASE,), attrs)
            self._param_cache[key] = ParamComponent
            return ParamComponent

        return type.__call__(self, *args, **kwargs)

    def __instancecheck__(self, instance):
        from comp.mods.helper.types import COMPONENT as BASE

        if not TYPE(instance) <= BASE:
            return False

        if self is BASE:
            return True

        types   = getattr(self, "_param_types", ())
        if types:
            domain = getattr(instance, "domain", None)
            if domain is None or tuple(domain) != types:
                return False

        cod = getattr(self, "_param_cod", None)
        if cod is not None:
            codom = getattr(instance, "codomain", None)
            from comp.mods.types.base import Jinja
            if not cod <= Jinja or not cod is codom:
                return False

        inner = getattr(self, "_param_inner", None)
        if inner is not None:
            if len(getattr(instance, "inner_vars", [])) != inner:
                return False

        content = getattr(self, "_param_content", None)
        if content is not None:
            if len(getattr(instance, "content_vars", [])) != content:
                return False

        return True

class _RESPONSIVE(TYPE(Typed)):
    _param_cache = {}

    def __call__(self, *args, **kwargs):
        if len(args) == 3 \
           and isinstance(args[0], str) \
           and isinstance(args[1], tuple) \
           and isinstance(args[2], dict):
            return type.__call__(self, *args, **kwargs)
        from comp.mods.types.base import Responsive as BASE

        if self is BASE:
            if args:
                types = args
                key   = ("pos", types)
                if key in self._param_cache:
                    return self._param_cache[key]
                class_name = f"{name(BASE)}({names(types)})"
                attrs = {
                    "__display__":    class_name,
                    "_param_types":   types,
                    "_param_kwargs":  None,
                }
                class CALL_RESPONSIVE(TYPE(BASE)):
                    def __instancecheck__(cls, instance):
                        from comp.models.responsive import Desktop, Tablet, Phone
                        return (
                            instance.desktop <= Desktop and
                            instance.tablet  <= Tablet  and
                            instance.phone   <= Phone   and
                            instance.desktop in types   and
                            instance.tablet  in types   and
                            instance.phone   in types
                        )
            if kwargs:
                expected = ("desktop", "tablet", "phone")
                if set(kwargs) != set(expected):
                    raise TypeError(f"Responsive[...] keywords must be {expected}")
                key = ("kw", tuple(sorted(kwargs.items())))
                if key in self._param_cache:
                    return self._param_cache[key]
                class_name = (
                    f"{name(BASE)}("
                    + ", ".join(f"{k}={name(v)}" for k, v in kwargs.items())
                    + ")"
                )
                attrs = {
                    "__display__":    class_name,
                    "_param_types":   None,
                    "_param_kwargs":  kwargs,
                }
                class CALL_RESPONSIVE(TYPE(BASE)):
                    def __instancecheck__(cls, instance):
                        return (
                            instance.desktop == kwargs['desktop'] and
                            instance.tablet  == kwargs['tablet']  and
                            instance.phone   == kwargs['phone']
                        )

            CallResposive = CALL_RESPONSIVE(class_name, (BASE,), attrs)
            self._param_cache[key] = CallResposive
            return CallResposive
        return type.__call__(self, *args, **kwargs)

    def __instancecheck__(cls, instance):
        if not isinstance(instance, MODEL):
            return False

        from comp.models.responsive import Desktop, Tablet, Phone

        return (
            (instance.desktop <= Desktop) and
            (instance.tablet <= Tablet) and
            (instance.phone <= Phone)
        )

        types = getattr(self, "_param_types", None)
        kws   = getattr(self, "_param_kwargs", None)

        if types is not None:
            for attr in ("desktop", "tablet", "phone"):
                if TYPE(getattr(instance, attr, None)) not in types:
                    return False
            return True

        else:
            for attr, required in kws.items():
                if TYPE(getattr(instance, attr, None)) is not required:
                    return False
            return True

class _RESPONSIVE_(_COMPONENT):
    def __instancecheck__(cls, instance):
        from comp.mods.types.base import Responsive, COMPONENT
        if not instance in COMPONENT:
            return False
        return all(x in Responsive for x in instance.domain)

    def __call__(cls, *args, **kwargs):
        if len(args) == 3 \
           and isinstance(args[0], str) \
           and isinstance(args[1], tuple) \
           and isinstance(args[2], dict):
            return type.__call__(cls, *args, **kwargs)

        from comp.mods.types.base import RESPONSIVE, COMPONENT, Responsive
        class _CALL_RESPONSIVE_(_COMPONENT):
            def __instancecheck__(cls, instance):
                if not instance in RESPONSIVE:
                    return False
                return all(x in Responsive(*args, **kwargs) for x in instance.domain)
        if args:
            class_name = f'RESPONSIVE({names(args)})'
        if kwargs:
            kws = ('desktop', 'tablet', 'phone')
            inner_name = [f"{k}={kwargs[k]}" for k in kws]
            class_name = f"RESPONSIVE({', '.join(inner_name)})"
        return _CALL_RESPONSIVE_(class_name, (COMPONENT,), {
            "__display__": class_name,
            "__null__": None
        })
