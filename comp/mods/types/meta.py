import re
from inspect import signature, Parameter, getsource
from jinja2 import Environment
from typed import (
    TYPE,
    Union,
    Str,
    Int,
    Bool,
    Any,
    Typed,
    Json,
    Prod,
    Dict,
    names,
    MODEL
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
        if not instance in Str or not instance in MODEL:
            return False
        return True

class _COMPONENT(TYPE(Typed)):
    _param_store = {}

    def __call__(cls, *types, cod=None, inner=None, content=None):
        key = (types, cod, inner, content)
        if key in cls._param_store:
            return cls._param_store[key]
        from comp.mods.helper.types import COMPONENT
        type_names = names(*types)
        name_parts = []
        if type_names:
            name_parts.append(type_names)
        if cod:
            name_parts.append(f"cod={getattr(cod, '__name__', str(cod))}")
        if inner is not None:
            name_parts.append(f"inner={inner}")
        if content is not None:
            name_parts.append(f"content={content}")
        clsname = f"COMPONENT[{', '.join(name_parts)}]"
        class _ParamComponent(COMPONENT):
            __display__ = clsname
            _param_types = types
            _param_cod = cod
            _param_inner = inner
            _param_content = content

            def __instancecheck__(self, instance):
                from comp.mods.helper.types import COMPONENT
                if not instance in COMPONENT:
                    return False
                if not TYPE(instance.codomain) <= JINJA:
                    return False
                if types:
                    if not getattr(instance, 'domain', None):
                        return False
                    if not all(isinstance(x, types) for x in domain):
                        for d, t in zip(domain, types):
                            if not isinstance(d, t):
                                return False
                if cod is not None:
                    if not cod <= _Jinja:
                        return False
                    if not instance.codomain <= cod:
                        return False
                if inner is not None:
                    n_inner = len(getattr(inst, 'inner_vars', []))
                    if n_inner != inner:
                        return False
                if content is not None:
                    n_content = len(getattr(inst, 'content_vars', []))
                    if n_content != content:
                        return False
                return True

        _ParamComponent.__name__ = clsname
        cls._param_store[key] = _ParamComponent
        return _ParamComponent

    def __instancecheck__(cls, instance):
        params = {k: getattr(cls, k, None) for k in ["_param_types", "_param_cod", "_param_inner", "_param_content"]}
        from comp.mods.helper.types import COMPONENT
        if not instance in COMPONENT:
            return False

        _types = params.get("_param_types", ())
        if _types:
            domain = getattr(instance, 'domain', None)
            if not domain:
                return False
            if not all(isinstance(x, _types) for x in domain):
                return False

        _cod = params.get("_param_cod")
        if _cod is not None:
            codom = getattr(instance, 'codomain', None)
            if codom:
                from comp.mods.types.meta import _Jinja
                try:
                    if not issubclass(_cod, _Jinja):
                        return False
                    if not issubclass(codom, _cod):
                        return False
                except Exception:
                    return False

        _inner = params.get("_param_inner")
        if _inner is not None:
            n_inner = len(getattr(instance, 'inner_vars', []))
            if n_inner != _inner:
                return False
        _content = params.get("_param_content")
        if _content is not None:
            n_content = len(getattr(instance, 'content_vars', []))
            if n_content != _content:
                return False
        return True

class _GRID_COMPONENT(_COMPONENT):
    def __instancecheck__(cls, instance):
        from comp.mods.helper.types import COMPONENT
        if not instance in COMPONENT:
            return False



def _check_page(page):
    from comp.service import render
    errors = []
    html = render(page)
    html_match = re.search(r"<html[^>]*>(.*?)</html>", html, flags=re.IGNORECASE | re.DOTALL)
    head_match = re.search(r"<head[^>]*>(.*?)</head>", html, flags=re.IGNORECASE | re.DOTALL)
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html, flags=re.IGNORECASE | re.DOTALL)

    if not html_match:
        errors.append("Missing <html> block.")
    if not head_match:
        errors.append("Missing <head> block.")
    if not body_match:
        errors.append("Missing <body> block.")

    if errors:
        err_text = "\n".join(errors)
        raise AssertionError(f"[check_page] Rendered HTML does not contain required block(s):\n{err_text}\nActual HTML:\n{html[:500]}...")

    html_content = html_match.group(1)

    html_outer_match = re.search(r"<html[^>]*>(.*?)</html>", html, flags=re.IGNORECASE | re.DOTALL)
    head_outer_match = re.search(r"<head[^>]*>(.*?)</head>", html, flags=re.IGNORECASE | re.DOTALL)
    body_outer_match = re.search(r"<body[^>]*>(.*?</body>)", html, flags=re.IGNORECASE | re.DOTALL)

    if not (html_outer_match and head_outer_match and body_outer_match):
        errors.append("One or more essential blocks (html, head, body) could not be located for structural analysis.")
    else:
        html_start, html_end = html_outer_match.span()
        head_start, head_end = head_outer_match.span()
        body_start, body_end = body_outer_match.span()

        if not (html_start < head_start < html_end and head_end < html_end):
            errors.append("<head> block is not contained within <html> block.")
        if not (html_start < body_start < html_end and body_end < html_end):
            errors.append("<body> block is not contained within <html> block.")

        html_opening_tag = re.match(r"<html[^>]*>", html, re.IGNORECASE)
        if html_opening_tag:
            text_before_head = html[html_opening_tag.end():head_start]
            if re.search(r"<[^/!][^>]*>", text_before_head): # Any open tag
                errors.append("<head> block is not a direct child of <html> (other tags found between them).")

            text_between_head_body = html[head_end:body_start]
            if re.search(r"<[^/!][^>]*>", text_between_head_body): # Any open tag
                errors.append("<body> block is not a direct child of <html> (other tags found between <head> and <body>).")
        else:
            errors.append("Could not find <html> opening tag for direct child check.")

        if body_start < head_start < body_end:
            errors.append("<head> block is found inside <body> block.")
        if head_start < body_start < head_end:
            errors.append("<body> block is found inside <head> block.")

    if errors:
        err_text = "\n".join(errors)
        raise AssertionError(f"[check_page] HTML structure validation failed:\n{err_text}\nActual HTML:\n{html[:500]}...")
    return True
