import re
from inspect import signature
from typed import typed, Bool, List, Str, Nill, Dict, Any, Extension, Url, Union
from markdown import markdown
from jinja2 import DictLoader, StrictUndefined, meta
from comp.mods.types.base import Content
from comp.mods.helper.helper import (
    _jinja,
    _jinja_env,
    _extract_raw_jinja,
    _render_jinja,
    _find_jinja_inner_vars,
    _find_jinja_vars
)
from comp.mods.helper.service import _style, _minify, _Preview
from comp.mods.err import RenderErr, MockErr
from comp.mods.types.base import COMPONENT, Jinja, PAGE
from comp.comps.includes import script as script_entity, asset as asset_entity
from comp.models import Script, Asset

@typed
def jinja_vars(entity: Union(Jinja, COMPONENT)) -> Dict(Any):
    if entity in Jinja:
        inner = _find_jinja_inner_vars(_extract_raw_jinja(entity))
        all_vars = set(_find_jinja_vars(entity))
        free_vars = tuple(sorted(all_vars - set(inner.keys())))
        return {"inner": inner, "free": free_vars}
    if entity in COMPONENT:
        return jinja_vars(_jinja(entity.jinja))

@typed
def jinja_inner_vars(entity: Union(Jinja, COMPONENT)) -> Dict(Any):
    return jinja_vars(entity)["inner"]

@typed
def jinja_free_vars(entity: Union(Jinja, COMPONENT)) -> Dict(Any):
    return jinja_vars(entity)["free"]

def render(
        entity: Union(Jinja, COMPONENT),
        __scripts__:    List(Script)=[],
        __assets__:     List(Asset)=[],
        __styled__:     Bool=True,
        __minified__:   Bool=False,
        **kwargs:       Dict(Any)
    ) -> Str:

    try:
        if entity in Jinja:
            return _render_jinja(entity, **kwargs)

        definer = getattr(entity, "func", entity)
        sig = signature(definer)
        valid_params = set(sig.parameters.keys())
        special = {"__scripts__", "__assets__", "__styled__"}
        valid_params = valid_params | special

        unknown_args = set(kwargs) - valid_params
        if unknown_args:
            raise TypeError(
                f"[render] Unexpected keyword argument(s) for '{getattr(definer, '__name__', definer)}': {', '.join(sorted(unknown_args))}\n"
                f"Allowed arguments: {', '.join(sorted(set(sig.parameters)))}"
            )

        kwargs.pop("__scripts__", None)
        kwargs.pop("__assets__", None)
        kwargs.pop("__styled__", None)

        content_params = {
            name: param
            for name, param in sig.parameters.items()
            if getattr(param, "annotation", None) is Content
        }
        for cname, param in content_params.items():
            if cname in kwargs:
                value = kwargs[cname]
                if isinstance(value, Str):
                    kwargs[cname] = markdown(value)
                elif isinstance(value, str) and value.lower().endswith(".md") and os.path.isfile(value):
                    md_text = file.read(value)
                    kwargs[cname] = markdown(md_text)
                else:
                    kwargs[cname] = markdown(value)

        call_args = {}
        for param in sig.parameters.values():
            if param.name in kwargs:
                call_args[param.name] = kwargs[param.name]
            elif param.default is not param.empty:
                call_args[param.name] = param.default
            else:
                call_args[param.name] = ""

        jinja = _extract_raw_jinja(entity(**call_args))

        script_tags = []
        for scr in __scripts__:
            script_src = scr.script_src
            if script_src in Extension('js') and not script_src in Url('http', 'https'):
                try:
                    with open(script_src, "r", encoding="utf-8") as f:
                        code = f.read()
                    tag = f"<script>{code}</script>"
                except Exception as e:
                    tag = f"<!-- [Could not read {script_src}: {e}] -->"
                script_tags.append(tag)
            else:
                tag = render(script_entity, script=scr, __styled__=False)
                script_tags.append(tag)
        scripts_insert = "\n".join(script_tags)

        asset_tags = []
        for ast in __assets__:
            href = getattr(ast, "asset_href", "")
            if href and href in Extension('css') and not href in Url('http', 'https'):
                try:
                    with open(href, "r", encoding="utf-8") as f:
                        code = f.read()
                    tag = f"<style>{code}</style>"
                except Exception as e:
                    tag = f"<!-- [Could not read {href}: {e}] -->"
                asset_tags.append(tag)
            elif href and href in Url('http', 'https'):
                tag = render(asset_entity, asset=ast, __styled__=False)
                asset_tags.append(tag)
            else:
                tag = render(asset_entity, asset=ast, __styled__=False)
                asset_tags.append(tag)
        assets_insert = "\n".join(asset_tags)

        head_pattern = re.compile(r'(<head\b[^>]*>)(.*?)(</head>)', re.IGNORECASE | re.DOTALL)
        def _insert_into_head(html_content, insert_str):
            m = head_pattern.search(html_content)
            if m:
                return html_content[:m.end(1)] + insert_str + m.group(2) + html_content[m.start(3):]
            return None

        if assets_insert:
            new_jinja = _insert_into_head(jinja, assets_insert)
            if new_jinja is not None:
                jinja = new_jinja
            else:
                jinja = assets_insert + jinja

        body_pattern = re.compile(r'(<body\b[^>]*>)(.*?)(</body>)', re.IGNORECASE | re.DOTALL)
        def _insert_into_body(html_content, insert_str):
            m = body_pattern.search(html_content)
            if m:
                return html_content[:m.start(3)] + insert_str + html_content[m.start(3):]
            return None

        if scripts_insert:
            new_jinja = _insert_into_body(jinja, scripts_insert)
            if new_jinja is not None:
                jinja = new_jinja
            else:
                jinja = jinja + scripts_insert

        context = {}
        context.update(call_args)
        context.update(kwargs)

        html = _render_jinja(jinja, **context)

        if __styled__:
            html = _style(html)
        if __minified__:
            html = _minify(html)

        return html
    except Exception as e:
        raise RenderErr(e)

@typed
def mock(entity: COMPONENT, **kwargs: Dict(Any)) -> PAGE:
    try:
        html = render(entity, **kwargs)
        html_match = re.search(r"<html[^>]*>(.*?)</html>", html, flags=re.IGNORECASE | re.DOTALL)
        head_match = re.search(r"<head[^>]*>(.*?)</head>", html, flags=re.IGNORECASE | re.DOTALL)
        body_match = re.search(r"<body[^>]*>(.*?)</body>", html, flags=re.IGNORECASE | re.DOTALL)

        if html_match and head_match and body_match:
            return entity

        from comp.mods.decorators import page
        def new_comp() -> Jinja:
            return f"""jinja
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
{html}
</body>
</html>
"""
        return page(new_comp)
    except Exception as e:
        raise MockErr(e)

preview = _Preview()

minify = _minify
