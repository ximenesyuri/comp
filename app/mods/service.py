import re
import webbrowser
from utils import cmd, file, path
from inspect import signature
from typed import typed, Bool, List, Str, Nill, Dict, Any, Extension, Url
from markdown import markdown
from jinja2 import Environment, DictLoader, StrictUndefined, meta
from bs4 import BeautifulSoup
from app.mods.types.base import Content
from app.mods.helper.service import _style, _minify, _resolve_deps
from app.mods.err import RenderErr, StyleErr, PreviewErr, MockErr
from app.mods.types.base import COMPONENT, Jinja, PAGE
from app.components import script as script_component, asset as asset_component
from app.models import Script, Asset


@typed
def render(
        component: COMPONENT,
        __scripts__: List(Script)=[],
        __assets__: List(Asset)=[],
        __styled__: Bool=True,
        __minified__: Bool=False,
        **kwargs: Dict(Any)
    ) -> Str:

    try:
        definer = getattr(component, "func", component)
        sig = signature(definer)
        valid_params = set(sig.parameters.keys())
        special = {"__scripts__", "__assets__", "depends_on", "__styled__"}
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
                    kwargs[cname] = md.to_html(value)
                elif isinstance(value, str) and value.lower().endswith(".md") and os.path.isfile(value):
                    md_text = file.read(value)
                    kwargs[cname] = markdown(md_text)
                else:
                    kwargs[cname] = markdown(value) 
        depends_on = []
        if "depends_on" in sig.parameters:
            depends_on_default = sig.parameters["depends_on"].default
            depends_on = kwargs.pop("depends_on", depends_on_default) or []
        if depends_on is None:
            depends_on = []
        all_depends_on = _resolve_deps(depends_on)
        call_args = {}
        for param in sig.parameters.values():
            if param.name == "depends_on":
                continue
            if param.name in kwargs:
                call_args[param.name] = kwargs[param.name]
            elif param.default is not param.empty:
                call_args[param.name] = param.default
            else:
                call_args[param.name] = ""
        if "depends_on" in sig.parameters:
            result = component(**call_args, depends_on=depends_on)
        else:
            result = component(**call_args)
        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], str):
            jinja_block_string, comp_locals = result
        else:
            jinja_block_string, comp_locals = result, {}

        if jinja_block_string.lstrip().startswith("jinja"):
            jinja_html = re.sub(r'^\s*jinja\s*\n?', '', jinja_block_string, count=1)
        else:
            jinja_html = jinja_block_string

        script_insertions = []

        for scr in __scripts__:
            script_src = scr.script_src
            if isinstance(script_src, Extension('js')) and not isinstance(script_src, Url('http', 'https')):
                try:
                    with open(script_src, "r", encoding="utf-8") as f:
                        code = f.read()
                    tag = f"<script>{code}</script>"
                except Exception as e:
                    tag = f"<!-- [Could not read {script_src}: {e}] -->"
                script_insertions.append(tag)
            else:
                tag = render(script_component, script=scr, __styled__=False)
                script_insertions.append(tag)

        asset_insertions = []
        for ast in __assets__:
            href = getattr(ast, "asset_href", "")
            if href and isinstance(href, Extension('css')) and not isinstance(href, Url('http', 'https')):
                try:
                    with open(href, "r", encoding="utf-8") as f:
                        code = f.read()
                    tag = f"<style>{code}</style>"
                except Exception as e:
                    tag = f"<!-- [Could not read {href}: {e}] -->"
                asset_insertions.append(tag)
            elif href and isinstance(href, Url('http', 'https')):
                tag = render(asset_component, asset=ast, __styled__=False)
                asset_insertions.append(tag)
            else:
                tag = render(asset_component, asset=ast, __styled__=False)
                asset_insertions.append(tag)

        inserts_html = "\n".join(asset_insertions + script_insertions) + ("\n" if asset_insertions or script_insertions else "")

        head_pat = re.compile(r'(<head\b[^>]*>)(.*?)(</head>)', re.IGNORECASE | re.DOTALL)
        def insert_into_head(html, insert_html):
            m = head_pat.search(html)
            if m:
                before = html[:m.end(1)]
                head_content = html[m.end(1):m.start(3)]
                after = html[m.start(3):]
                return before + insert_html + head_content + after
            return None

        if "<head" in jinja_html.lower():
            new_html = insert_into_head(jinja_html, inserts_html)
            if new_html is not None:
                jinja_html = new_html
            else:
                jinja_html = inserts_html + jinja_html
        else:
            jinja_html = inserts_html + jinja_html

        full_jinja_context = dict(comp_locals)
        full_jinja_context.update(call_args)
        full_jinja_context.update(kwargs)
        for dep in all_depends_on:
            dep_name = getattr(dep, "__name__", str(dep))
            def make_rendered_dep_func(dep):
                def _inner(*a, **kw):
                    dep_sig = signature(getattr(dep, "func", dep))
                    dep_param_names = set(dep_sig.parameters.keys())
                    dep_kwargs = {k: v for k, v in full_jinja_context.items() if k in dep_param_names}
                    dep_kwargs.update(kw)
                    return render(dep, **dep_kwargs, __styled__=False)
                return _inner
            full_jinja_context[dep_name] = make_rendered_dep_func(dep)

        template_name = getattr(definer, '__name__', 'template')
        env = Environment(loader=DictLoader({template_name: jinja_html}), undefined=StrictUndefined)
        template = env.get_template(template_name)
        rendered_component = template.render(**full_jinja_context)

        if __styled__:
            rendered_component = _style(rendered_component)
        if __minified__:
            rendered_component = _minify(rendered_component)
        return rendered_component
    except Exception as e:
        raise RenderErr(e)

@typed
def mock(component: COMPONENT, **kwargs: Dict(Any)) -> PAGE:
    try:
        html = render(component, **kwargs)
        html_match = re.search(r"<html[^>]*>(.*?)</html>", html, flags=re.IGNORECASE | re.DOTALL)
        head_match = re.search(r"<head[^>]*>(.*?)</head>", html, flags=re.IGNORECASE | re.DOTALL)
        body_match = re.search(r"<body[^>]*>(.*?)</body>", html, flags=re.IGNORECASE | re.DOTALL)

        if html_match and head_match and body_match:
            return component

        from app.mods.decorators.base import page
        def new_definer() -> Jinja:
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
        return page(new_definer)
    except Exception as e:
        raise MockErr(e)

@typed
def preview(component: COMPONENT, **kwargs: Dict(Any)) -> Nill:
    try:
        html = render(component, **kwargs)
        temp_file = "/tmp/app_preview_component.html"
        file.write(
            filepath=temp_file,
            content=html
        )
        webbrowser.open_new_tab(f'file://{path.abs(temp_file)}')
    except Exception as e:
        raise PreviewErr(e)
