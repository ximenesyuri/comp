import re
import functools
import webbrowser
from inspect import signature, Parameter
from typed import typed, Union, List, Str, Nill, Dict, Any, Tuple
from markdown import markdown
from jinja2 import Environment, DictLoader, StrictUndefined, meta
from bs4 import BeautifulSoup
from app.mods.types.base import Content
from app.mods.helper.helper import _jinja_regex
from app.mods.helper.types  import _PAGE, _STATIC_PAGE
from app.mods.err import RenderErr, BuildErr, StyleErr, PreviewErr, MockErr
from app.mods.types.base import COMPONENT, Jinja, STATIC, PAGE, STATIC_PAGE, Inner
from app.components import script as script_component, asset as asset_component
from app.models import Script, Asset

def orig_render(component: COMPONENT, **vars) -> Str:
    """
    Renders the given component, passing keyword argument variables.
    Handles Inner defaults, model coercion, context construction,
    supports depends_on, and dependency injection as in the legacy version.
    """
    try:
        definer = getattr(component, "func", component)
        context = dict(vars)
        sig = signature(definer)
        params = list(sig.parameters.values())
        depends_on = []
        if 'depends_on' in sig.parameters:
            depends_on_default = sig.parameters['depends_on'].default
            depends_on = context.pop('depends_on', depends_on_default) or []
        if depends_on is None:
            depends_on = []
        if not isinstance(depends_on, (list, tuple, set)):
            raise TypeError("depends_on must be a list, tuple, or set.")

        # Prepare call_args for the definer
        call_args = {}
        for param in params:
            if param.name == "depends_on":
                continue
            if param.name in context:
                val = context[param.name]
                # Try model auto-coercion if needed
                if (hasattr(param.annotation, '__name__')
                        and (param.annotation.__name__.startswith("Model") or param.annotation.__name__.endswith("MODEL"))):
                    from typed.models import MODEL
                    ann = param.annotation
                    if (not isinstance(val, ann)) and isinstance(val, dict):
                        val = ann(val)
                call_args[param.name] = val
            elif param.default is not param.empty:
                call_args[param.name] = param.default
            elif getattr(param.annotation, '__name__', '') == 'Inner':
                call_args[param.name] = ''
            else:
                raise TypeError(f"Missing required argument '{param.name}' for component '{definer.__name__}'")

        # Actually call the definer/component (with or without depends_on)
        if 'depends_on' in sig.parameters:
            result = definer(**call_args, depends_on=depends_on)
        else:
            result = definer(**call_args)

        # Accept both "jinja string" or "(jinja string, locals)"
        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], str) and isinstance(result[1], dict):
            jinja_block_string, comp_locals = result
        else:
            jinja_block_string, comp_locals = result, {}

        from app.mods.helper.helper import _jinja_regex
        regex_str = re.compile(_jinja_regex(), re.DOTALL)
        match = regex_str.match(jinja_block_string)
        if not match:
            raise TypeError("Invalid Jinja block string format.")
        jinja_content = match.group(1)
        template_name = getattr(definer, '__name__', 'template')

        def make_rendered_dep_func(dep):
            def _inner(*args, **kwargs):
                from inspect import signature
                sig2 = signature(dep)
                param_names = [p.name for p in sig2.parameters.values()]
                child_context = dict(context)
                for i, value in enumerate(args):
                    if i < len(param_names):
                        child_context[param_names[i]] = value
                child_context.update(kwargs)
                dep_args = {}
                for p in sig2.parameters.values():
                    if p.name in child_context:
                        dep_args[p.name] = child_context[p.name]
                    elif p.default is not Parameter.empty:
                        dep_args[p.name] = p.default
                dep_block = dep(**dep_args)
                dep_match = re.compile(_jinja_regex(), re.DOTALL).match(dep_block)
                if not dep_match:
                    raise TypeError(f"Invalid Jinja block string format in dependency {dep.__name__}")
                dep_jinja_content = dep_match.group(1)
                from jinja2 import Environment, StrictUndefined
                env2 = Environment(undefined=StrictUndefined)
                dep_template = env2.from_string(dep_jinja_content)
                return dep_template.render(**child_context)
            return _inner

        # Compose the jinja context: priority = comp_locals < call_args < input vars
        full_jinja_context = dict(comp_locals)
        full_jinja_context.update(call_args)
        full_jinja_context.update(vars)

        for dep in depends_on:
            if not callable(dep):
                raise TypeError(f"Dependency {repr(dep)} is not a definer (function)")
            dep_name = getattr(dep, '__name__', str(dep))
            full_jinja_context[dep_name] = make_rendered_dep_func(dep)

        from jinja2 import Environment, DictLoader, StrictUndefined
        env = Environment(
            loader=DictLoader({template_name: jinja_content}),
            undefined=StrictUndefined
        )
        template = env.get_template(template_name)
        return template.render(**full_jinja_context)
    except Exception as e:
        from app.mods.err import RenderErr
        raise RenderErr(e)

@typed
def render(component: COMPONENT, __scripts__: List(Script)=[], __assets__: List(Asset)=[], **kwargs: Dict(Any)) -> Str:
    """
    Enhanced render: supports __scripts__, __assets__ and pre-processing Content parameters.
    """
    definer = getattr(component, "func", component)
    sig = signature(definer)
    valid_params = set(sig.parameters.keys())
    special = {"__scripts__", "__assets__", "depends_on"}
    valid_params = valid_params | special

    unknown_args = set(kwargs.keys()) - valid_params
    if unknown_args:
        raise TypeError(f"[render] Unexpected keyword argument(s) for '{getattr(definer, '__name__', definer)}': {', '.join(sorted(unknown_args))}\n"
                        f"Allowed arguments: {', '.join(sorted(set(sig.parameters)))}")

    kwargs.pop("__scripts__", None)
    kwargs.pop("__assets__", None)

    definer = getattr(component, "func", component)
    sig = signature(definer)
    params = sig.parameters
    from typed.models import MODEL
    content_params = {name: param for name, param in params.items()
                             if getattr(param, "annotation", None) is Content}

    for cname, param in content_params.items():
        if cname not in kwargs:
            continue
        value = kwargs[cname]
        if isinstance(value, Str):
            kwargs[cname] = markdown(value)
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
    call_args = {}
    for param in params.values():
        if param.name == "depends_on":
            continue
        if param.name in kwargs:
            call_args[param.name] = kwargs[param.name]
        elif param.default is not param.empty:
            call_args[param.name] = param.default
        else:
            call_args[param.name] = ""
    if "depends_on" in params:
        result = definer(**call_args, depends_on=depends_on)
    else:
        result = definer(**call_args)
    if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], str):
        jinja_block_string, comp_locals = result
    else:
        jinja_block_string, comp_locals = result, {}

    script_insertions = []
    for scr in __scripts__:
        src = getattr(scr, "script_src", "")
        if src and isinstance(src, str) and src.endswith(".js") and not src.startswith("http"):
            try:
                with open(Path(src), "r", encoding="utf-8") as f:
                    code = f.read()
                tag = f"<script>{code}</script>"
            except Exception as e:
                tag = f"<!-- [Could not read {src}: {e}] -->"
            script_insertions.append(tag)
        elif src and (src.startswith("http://") or src.startswith("https://")):
            tag = orig_render(script_component, script=scr)
            script_insertions.append(tag)
        else:
            tag = orig_render(script_component, script=scr)
            script_insertions.append(tag)

    asset_insertions = []
    for ast in __assets__:
        href = getattr(ast, "asset_href", "")
        mime = getattr(ast, "asset_mime", "")
        if href and isinstance(href, str) and href.endswith(".css") and not href.startswith("http"):
            try:
                with open(Path(href), "r", encoding="utf-8") as f:
                    code = f.read()
                tag = f"<style>{code}</style>"
            except Exception as e:
                tag = f"<!-- [Could not read {href}: {e}] -->"
            asset_insertions.append(tag)
        elif href and (href.startswith("http://") or href.startswith("https://")):
            tag = orig_render(asset_component, asset=ast)
            asset_insertions.append(tag)
        else:
            tag = orig_render(asset_component, asset=ast)
            asset_insertions.append(tag)

    head_pat = re.compile(r'(<head\b[^>]*>)(.*?)(</head>)', re.IGNORECASE | re.DOTALL)
    def insert_into_head(html, insert_html):
        m = head_pat.search(html)
        if m:
            before = html[:m.end(1)]
            head_content = html[m.end(1):m.start(3)]
            after = html[m.start(3):]
            return before + "".join(insert_html) + head_content + after
        return None

    if jinja_block_string.lstrip().startswith("jinja"):
        jinja_html = re.sub(r'^\s*jinja\s*\n?', '', jinja_block_string, count=1)
    else:
        jinja_html = jinja_block_string
    joined_inserts = asset_insertions + script_insertions
    if "<head" in jinja_html.lower():
        new_html = insert_into_head(jinja_html, joined_inserts)
        if new_html is not None:
            jinja_html = new_html
        else:
            jinja_html = "\n".join(joined_inserts) + "\n" + jinja_html
    else:
        jinja_html = "\n".join(joined_inserts) + "\n" + jinja_html

    full_jinja_context = dict(comp_locals)
    full_jinja_context.update(call_args)
    full_jinja_context.update(kwargs)
    for dep in depends_on:
        dep_name = getattr(dep, "__name__", str(dep))
        def make_rendered_dep_func(dep):
            def _inner(*a, **kw):
                return orig_render(dep, **full_jinja_context)
            return _inner
        full_jinja_context[dep_name] = make_rendered_dep_func(dep)
    from jinja2 import Environment, DictLoader, StrictUndefined
    template_name = getattr(definer, '__name__', 'template')
    env = Environment(loader=DictLoader({template_name: jinja_html}), undefined=StrictUndefined)
    template = env.get_template(template_name)
    return template.render(**full_jinja_context)

@typed
def style(page: Union(PAGE, STATIC_PAGE)) -> Union(PAGE, STATIC_PAGE):
    try:
        if not page.get("auto_style", False):
            return page

        current_page = page
        if isinstance(page, STATIC_PAGE):
            from app.service import build
            component_to_render = build(STATIC(page))
        else:
            component_to_render = page

        html_content = render(component_to_render)
        soup = BeautifulSoup(html_content, 'html.parser')

        def escape_class_selector(cls):
            return cls.replace(':', '\\:').replace('#', '\\#').replace('[', '\\[').replace(']', '\\]').replace('.', '\\.')

        PREFIXES_MAP = {
            "phone":   "(min-width: 0px) and (max-width: 767px)",
            "tablet":  "(min-width: 768px) and (max-width: 1024px)",
            "mobile":  "(min-width: 0px) and (max-width: 1024px)",
            "desktop": "(min-width: 1025px) and (max-width: 10000px)"
        }
        ALIAS_MAP = {
            "p": "phone",
            "t": "tablet",
            "m": "mobile",
            "d": "desktop",
            "n": "not"
        }
        VALID_MEDIA_PREFIXES_AND_ALIASES = set(PREFIXES_MAP.keys()).union(ALIAS_MAP.keys())
        IMPORTANT_FLAG = "!"
        NOT_FLAG = "not"
        NOT_ALIASES = ["n"]

        found_styles = {}

        patterns = {
            'margin_padding': re.compile(r'(m[tblr]|p[tblr])-(\d+(?:\.\d+)?)(px|vh|vw|em|rem|%)'),
            'border': re.compile(r'b(t|b|r|l)-(\d+(?:\.\d+)?)(px|em|rem|%)?-(\w+)'),
            'font_size': re.compile(r'fz-(\d+(?:\.\d+)?)(px|em|rem|%)'),
            'font_weight': re.compile(r'fw-(extra-light|el|light|l|normal|n|bold|b|extra-bold|eb|black|B|\d{3})'),
            'font_family': re.compile(r'ff-\[(.+?)\]'),
            'font_style': re.compile(r'fs-(italic|it|normal|oblique)'),
            'text_decoration': re.compile(r'td-(underline|u|overline|o|line-through|lt|none)'),
            'letter_spacing': re.compile(r'ls-(\d+(?:\.\d+)?)(em|px|rem|%)'),
            'color_hex_rgb': re.compile(r'fc-(#([0-9a-fA-F]{3}){1,2}|rgb\((\d{1,3},\d{1,3},\d{1,3})\))'),
            'color_var': re.compile(r'fc-([a-zA-Z][a-zA-Z0-9_\-]+)'),
            'fill_hex_rgb': re.compile(r'fill-(#([0-9a-fA-F]{3}){1,2}|rgb\((\d{1,3},\d{1,3},\d{1,3})\))'),
            'fill_var': re.compile(r'fill-([a-zA-Z][a-zA-Z0-9_\-]+)'),
            'text_transform': re.compile(r'tt-(cap|up|upper|lw|low|lower)'),
            'width': re.compile(r'w-(full|auto|none|\d+(?:\.\d+)?(?:px|%|vw|vh|em|rem))'), # width
            'height': re.compile(r'h-(full|auto|none|\d+(?:\.\d+)?(?:px|%|vw|vh|em|rem))'), # height
            'min_width': re.compile(r'mw-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'), # min-width
            'max_width': re.compile(r'Mw-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'), # max-width
            'min_height': re.compile(r'mh-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'), # min-height
            'max_height': re.compile(r'Mh-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'), # max-height
            'gap': re.compile(r'gap-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'), # gap
            'border_radius': re.compile(r'(radius|bR)-(\d+(?:\.\d+)?)(px|%|em|rem)'), # border-radius
            'z_index': re.compile(r'z-(full|none|\d+)'), # z-index
            'background_color_hex_rgb': re.compile(r'bg-(#([0-9a-fA-F]{3}){1,2}|rgb\((\d{1,3},\s*\d{1,3},\s*\d{1,3})\))'),
            'background_size': re.compile(r'bg-sz-(\d+(?:\.\d+)?)(px|%|em|rem)'),
            'background_blur': re.compile(r'(?:bg-blur|blur)-(\d+(?:\.\d+)?)(px|em|rem|%)'),
            'display': re.compile(r'^(?:flex|fl|inline|inl|block|blk|table|tab|inline-block|inl-blk|inline-flex|inl-fl)$'),
            'position': re.compile(r'pos-(fix|abs|rel|stk)'),
            'text_justify': re.compile(r'(?:just|jst)-(start|st|end|ed|left|lft|right|rgt|center|cnt)'),
            'overflow_x': re.compile(r'over-x'),
            'overflow_y': re.compile(r'over-y'),
            'scroll_x': re.compile(r'(?:scroll|scl)-x'),
            'scroll_y': re.compile(r'(?:scroll|scl)-y'),
            'scroll_all': re.compile(r'(?:scroll|scl)$'),
        }

        style_property_map = {
            'mt': 'margin-top', 'mb': 'margin-bottom', 'ml': 'margin-left', 'mr': 'margin-right',
            'pt': 'padding-top', 'pb': 'padding-bottom', 'pl': 'padding-left', 'pr': 'padding-right',
            'bt': 'border-top', 'bb': 'border-bottom', 'br': 'border-right', 'bl': 'border-left',
            'fz': 'font-size',
            'fw': 'font-weight',
            'ff': 'font-family',
            'fs': 'font-style',
            'td': 'text-decoration',
            'ls': 'letter-spacing',
            'fc': 'color',
            'tt': 'text-transform',
            'w': 'width',
            'h': 'height',
            'mw': 'min-width',
            'Mw': 'max-width',
            'mh': 'min-height',
            'Mh': 'max-height',
            'gap': 'gap',
            'radius': 'border-radius', 'bR': 'border-radius',
            'z': 'z-index',
            'bg': 'background-color',
            'bg-sz': 'background-size',
            'bg-blur': 'backdrop-filter',
            'fl': 'display', 'inl': 'display', 'blk': 'display', 'tab': 'display',
            'inl-blk': 'display', 'inl-fl': 'display',
            'pos': 'position',
            'just': 'text-align',
            'over-x': 'overflow-x',
            'over-y': 'overflow-y',
            'scroll-x': 'position',
            'scroll-y': 'position',
            'scroll': 'position',
        }

        font_weight_map = {
            'extra-light': 200, 'el': 200,
            'light': 300, 'l': 300,
            'normal': 400, 'n': 400,
            'bold': 700, 'b': 700,
            'extra-bold': 800, 'eb': 800,
            'black': 900, 'B': 900,
        }

        font_style_map = {
            'italic': 'italic', 'it': 'italic',
            'normal': 'normal',
            'oblique': 'oblique',
        }

        text_decoration_map = {
            'underline': 'underline', 'u': 'underline',
            'overline': 'overline', 'o': 'overline',
            'line-through': 'line-through', 'lt': 'line-through',
            'none': 'none',
        }

        text_transform_map = {
            'cap': 'capitalize',
            'up': 'uppercase', 'upper': 'uppercase',
            'lw': 'lowercase', 'low': 'lowercase', 'lower': 'lowercase',
        }

        display_map = {
            'flex': 'flex', 'fl': 'flex',
            'inline': 'inline', 'inl': 'inline',
            'block': 'block', 'blk': 'block',
            'table': 'table', 'tab': 'table',
            'inline-block': 'inline-block', 'inl-blk': 'inline-block',
            'inline-flex': 'inline-flex', 'inl-fl': 'inline-flex',
        }

        position_map = {
            'fix': 'fixed',
            'abs': 'absolute',
            'rel': 'relative',
            'stk': 'sticky',
        }

        text_justify_map = {
            'start': 'start', 'st': 'start',
            'end': 'end', 'ed': 'end',
            'left': 'left', 'lft': 'left',
            'right': 'right', 'rgt': 'right',
            'center': 'center', 'cnt': 'center',
        }


        def style_for_base_class(class_name):
            css_rule = None
            match = patterns['margin_padding'].match(class_name)
            if match:
                prefix, value, unit = match.groups()
                prop = style_property_map[prefix]
                css_rule = f"{prop}: {value}{unit};"
            if not css_rule:
                match = patterns['border'].match(class_name)
                if match:
                    border_type, value, unit, color_or_style = match.groups()
                    prop = style_property_map['b' + border_type]
                    unit = unit if unit else 'px'  # Default unit for border width
                    css_rule = f"{prop}: {value}{unit} {color_or_style};"
            if not css_rule:
                match = patterns['font_size'].match(class_name)
                if match:
                    value, unit = match.groups()
                    prop = style_property_map['fz']
                    css_rule = f"{prop}: {value}{unit};"
            if not css_rule:
                match = patterns['font_weight'].match(class_name)
                if match:
                    weight_key = match.group(1)
                    prop = style_property_map['fw']
                    weight_val = font_weight_map.get(weight_key)
                    if weight_val is None:
                        try:
                            weight_val = int(weight_key)
                        except ValueError:
                            weight_val = weight_key
                    css_rule = f"{prop}: {weight_val};"
            if not css_rule:
                match = patterns['font_family'].match(class_name)
                if match:
                    font_families_encoded = match.group(1)
                    font_families_decoded = font_families_encoded.replace('_', ' ')
                    prop = style_property_map['ff']
                    css_rule = f"{prop}: {font_families_decoded};"
            if not css_rule:
                match = patterns['font_style'].match(class_name)
                if match:
                    style_key = match.group(1)
                    prop = style_property_map['fs']
                    style_val = font_style_map.get(style_key, style_key)
                    css_rule = f"{prop}: {style_val};"
            if not css_rule:
                match = patterns['text_decoration'].match(class_name)
                if match:
                    decoration_key = match.group(1)
                    prop = style_property_map['td']
                    decoration_val = text_decoration_map.get(decoration_key, decoration_key)
                    css_rule = f"{prop}: {decoration_val};"
            if not css_rule:
                match = patterns['letter_spacing'].match(class_name)
                if match:
                    value, unit = match.groups()
                    prop = style_property_map['ls']
                    css_rule = f"{prop}: {value}{unit};"
            if not css_rule:
                match = patterns['color_hex_rgb'].match(class_name)
                if match:
                    color_val = match.group(1)
                    prop = style_property_map['fc']
                    css_rule = f"{prop}: {color_val};"
            if not css_rule:
                match = patterns['color_var'].match(class_name)
                if match:
                    var_name = match.group(1).replace('-', '_')
                    prop = style_property_map['fc']
                    css_rule = f"{prop}: var(--{var_name});"
            if not css_rule:
                match = patterns['fill_hex_rgb'].match(class_name)
                if match:
                    color_val = match.group(1)
                    css_rule = f"fill: {color_val};"
            if not css_rule:
                match = patterns['fill_var'].match(class_name)
                if match:
                    var_name = match.group(1).replace('-', '_')
                    prop = style_property_map['fill']
                    css_rule = f"fill: var(--{var_name});"
            if not css_rule:
                match = patterns['text_transform'].match(class_name)
                if match:
                    transform_key = match.group(1)
                    prop = style_property_map['tt']
                    transform_val = text_transform_map.get(transform_key)
                    css_rule = f"{prop}: {transform_val};"
            if not css_rule:
                match = patterns['width'].match(class_name)
                if match:
                    value_str = match.group(1)
                    if value_str == 'full':
                        css_val = '100%'
                    elif value_str == 'auto':
                        css_val = 'auto'
                    elif value_str == 'none':
                        css_val = 'none'
                    else:
                        css_val = value_str
                    prop = style_property_map['w']
                    css_rule = f"{prop}: {css_val};"
            if not css_rule:
                match = patterns['height'].match(class_name)
                if match:
                    value_str = match.group(1)
                    if value_str == 'full':
                        css_val = '100%'
                    elif value_str == 'auto':
                        css_val = 'auto'
                    elif value_str == 'none':
                        css_val = 'none'
                    else:
                        css_val = value_str
                    prop = style_property_map['h']
                    css_rule = f"{prop}: {css_val};"
            if not css_rule:
                match = patterns['min_width'].match(class_name)
                if match:
                    value, unit = match.groups()
                    prop = style_property_map['mw']
                    css_rule = f"{prop}: {value}{unit};"
            if not css_rule:
                match = patterns['max_width'].match(class_name)
                if match:
                    value, unit = match.groups()
                    prop = style_property_map['Mw']
                    css_rule = f"{prop}: {value}{unit};"
            if not css_rule:
                match = patterns['min_height'].match(class_name)
                if match:
                    value, unit = match.groups()
                    prop = style_property_map['mh']
                    css_rule = f"{prop}: {value}{unit};"
            if not css_rule:
                match = patterns['max_height'].match(class_name)
                if match:
                    value, unit = match.groups()
                    prop = style_property_map['Mh']
                    css_rule = f"{prop}: {value}{unit};"
            if not css_rule:
                match = patterns['gap'].match(class_name)
                if match:
                    value, unit = match.groups()
                    prop = style_property_map['gap']
                    css_rule = f"{prop}: {value}{unit};"
            if not css_rule:
                match = patterns['border_radius'].match(class_name)
                if match:
                    prefix, value, unit = match.groups()
                    prop = style_property_map[prefix]
                    css_rule = f"{prop}: {value}{unit};"
            if not css_rule:
                match = patterns['z_index'].match(class_name)
                if match:
                    value_str = match.group(1)
                    if value_str == 'full':
                        css_val = '100000'
                    elif value_str == 'none':
                        css_val = '0'
                    else:
                        css_val = value_str
                    prop = style_property_map['z']
                    css_rule = f"{prop}: {css_val};"
            if not css_rule:
                match = patterns['background_color_hex_rgb'].match(class_name)
                if match:
                    bg_color_val = match.group(1)
                    css_rule = f"background-color: {bg_color_val};"
            if not css_rule:
                match = patterns['background_size'].match(class_name)
                if match:
                    value, unit = match.groups()
                    css_rule = f"background-size: {value}{unit};"
            if not css_rule:
                match = patterns['background_blur'].match(class_name)
                if match:
                    value, unit = match.groups()
                    css_rule = f"backdrop-filter: blur({value}{unit}); background: rgba(0, 0, 0, 0.2);"
            if not css_rule:
                match = patterns['display'].match(class_name)
                if match:
                    display_val = display_map.get(class_name)
                    if display_val:
                        css_rule = f"display: {display_val};"
            if not css_rule:
                match = patterns['position'].match(class_name)
                if match:
                    pos_key = match.group(1)
                    pos_val = position_map.get(pos_key)
                    if pos_val:
                        css_rule = f"position: {pos_val};"
            if not css_rule:
                match = patterns['text_justify'].match(class_name)
                if match:
                    justify_key = match.group(1)
                    justify_val = text_justify_map.get(justify_key)
                    if justify_val:
                        css_rule = f"text-align: {justify_val};"
            if not css_rule:
                if class_name in ['flex-center', 'fl-cnt', 'fl-center', 'flex-cnt']:
                    css_rule = "display: flex; justify-content: center; align-items: center;"
            if not css_rule:
                match = patterns['overflow_x'].match(class_name)
                if match:
                    css_rule = "overflow-x: auto;"
            if not css_rule:
                match = patterns['overflow_y'].match(class_name)
                if match:
                    css_rule = "overflow-y: auto;"
            if not css_rule:
                match = patterns['scroll_x'].match(class_name)
                if match:
                    css_rule = "position: fixed; overflow-x: auto; max-height: 100vh;"
            if not css_rule:
                match = patterns['scroll_y'].match(class_name)
                if match:
                    css_rule = "position: fixed; overflow-y: auto; max-height: 100vh;"
            if not css_rule:
                match = patterns['scroll_all'].match(class_name)
                if match:
                    css_rule = "position: fixed; overflow-x: auto; overflow-y: auto; max-height: 100vh;"
            return css_rule

        for tag in soup.find_all(True):
            if tag.has_attr('class'):
                for class_name in tag['class']:
                    media_pref = None
                    is_important = False
                    is_not_prefixed = False
                    parts = class_name.split(':')
                    current_parts_idx = 0

                    if parts[current_parts_idx] == IMPORTANT_FLAG:
                        is_important = True
                        current_parts_idx += 1

                    if current_parts_idx < len(parts) and (parts[current_parts_idx] == NOT_FLAG or parts[current_parts_idx] in NOT_ALIASES):
                        is_not_prefixed = True
                        current_parts_idx += 1

                    if current_parts_idx < len(parts):
                        potential_media_prefix = parts[current_parts_idx]
                        if potential_media_prefix in VALID_MEDIA_PREFIXES_AND_ALIASES:
                            media_pref = ALIAS_MAP.get(potential_media_prefix, potential_media_prefix)
                            current_parts_idx += 1
                    base_class_name = ":".join(parts[current_parts_idx:])

                    css_rule = style_for_base_class(base_class_name)
                    if css_rule:
                        if is_important:
                            css_rule = css_rule.replace(';', ' !important;')
                        found_styles[(media_pref, is_important, is_not_prefixed, class_name)] = css_rule

        CANONICAL_MEDIA_NAMES = ["phone", "tablet", "mobile", "desktop"]
        css_buckets = {
            name: {
                False: {False: [], True: []},
                True: {False: [], True: []}
            } for name in CANONICAL_MEDIA_NAMES
        }
        css_buckets[None] = {
            False: {False: [], True: []},
            True: {False: [], True: []}
        }

        for (pref, is_important, is_not_prefixed, original_class_name), css_rule in found_styles.items():
            canonical_pref_for_bucket = pref 
            selector = '.' + escape_class_selector(original_class_name)
            rule_str = f"{selector} {{\n    {css_rule}\n}}"
            if canonical_pref_for_bucket in css_buckets and \
               is_important in css_buckets[canonical_pref_for_bucket] and \
               is_not_prefixed in css_buckets[canonical_pref_for_bucket][is_important]:
                css_buckets[canonical_pref_for_bucket][is_important][is_not_prefixed].append(rule_str)
            else:
                print(f"Warning: Rule for '{original_class_name}' with (pref={pref}, imp={is_important}, not={is_not_prefixed}) could not be placed in bucket. Defaulting to global non-important non-not.")
                css_buckets[None][False][False].append(rule_str)
        new_css_rules_list = []
        new_css_rules_list.extend(css_buckets[None][False][False])
        new_css_rules_list.extend(css_buckets[None][True][False])
        for canonical_media_name in CANONICAL_MEDIA_NAMES:
            mq_expression = PREFIXES_MAP[canonical_media_name]

            rules_for_this_mq = []
            rules_for_this_mq.extend(css_buckets[canonical_media_name][False][False])
            rules_for_this_mq.extend(css_buckets[canonical_media_name][True][False])

            if rules_for_this_mq:
                new_css_rules_list.append(f"@media {mq_expression} {{\n" + "\n".join(rules_for_this_mq) + "\n}\n")
            not_rules_for_this_mq = []
            not_rules_for_this_mq.extend(css_buckets[canonical_media_name][False][True])
            not_rules_for_this_mq.extend(css_buckets[canonical_media_name][True][True])

            if not_rules_for_this_mq:
                not_mq_expression = ""
                if canonical_media_name == "phone":
                    not_mq_expression = "(min-width: 768px)"
                elif canonical_media_name == "tablet":
                    not_mq_expression = "(max-width: 767px), (min-width: 1025px)"
                elif canonical_media_name == "mobile":
                    not_mq_expression = "(min-width: 1025px)"
                elif canonical_media_name == "desktop":
                    not_mq_expression = "(max-width: 1024px)"

                if not_mq_expression:
                    new_css_rules_list.append(f"@media {not_mq_expression} {{\n" + "\n".join(not_rules_for_this_mq) + "\n}\n")
                else:
                    print(f"Warning: Could not create 'not' media query for '{canonical_media_name}' for classes: {not_rules_for_this_mq}")

        new_css_rules = "\n".join(new_css_rules_list)

        head_tag = soup.find('head')
        if not head_tag:
            print("Warning: No <head> tag found in the HTML. Cannot inject styles.")
            return page

        style_tag = head_tag.find('style')
        if style_tag:
            if style_tag.string:
                style_tag.string += new_css_rules
            else:
                style_tag.string = new_css_rules
        elif new_css_rules:
            new_style_tag = soup.new_tag("style")
            new_style_tag.string = new_css_rules
            head_tag.append(new_style_tag)

        modified_html = str(soup)
        original_definer = page["definer"]
        from app.mods.types import Jinja
        final_jinja_str = f"jinja\n{modified_html}"

        from app import definer
        @definer
        def new_definer() -> Jinja:
            return final_jinja_str

        if hasattr(original_definer, '__name__'):
            new_definer.__name__ = original_definer.__name__ + "_styled"
        if hasattr(original_definer, '__annotations__'):
            new_definer.__annotations__ = original_definer.__annotations__

        return page.__class__({**page, "definer": new_definer})
    except Exception as e:
        raise StyleErr(e)

@typed
def mock(component: Union(COMPONENT, STATIC)) -> Union(PAGE, STATIC_PAGE):
    """
    1. If the component (resp. static) is not a page (resp. static page),
       turn it into a page (resp. static page) with auto_style=True by adding
       <html>, <head>, and <body> blocks. The original content of the component
       should be introduced inside the <body> block.
    2. If the component is a page (resp. static page), do nothing.
    """
    try:
        if isinstance(component, STATIC):
            component_to_render = build(component)
        else:
            component_to_render = component

        html = render(component_to_render)
        html_match = re.search(r"<html[^>]*>(.*?)</html>", html, flags=re.IGNORECASE | re.DOTALL)
        head_match = re.search(r"<head[^>]*>(.*?)</head>", html, flags=re.IGNORECASE | re.DOTALL)
        body_match = re.search(r"<body[^>]*>(.*?)</body>", html, flags=re.IGNORECASE | re.DOTALL)

        if html_match and head_match and body_match:
            return component

        definer = component_to_render["definer"]
        context = component_to_render["context"]

        from app import definer
        @definer
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
        if isinstance(component, COMPONENT):
            page = PAGE(
                definer=new_definer,
                context=context,
                static_dir="",
                auto_style=True,
            )
            return page
        elif isinstance(component, STATIC):
            return STATIC_PAGE(
                definer=new_definer,
                context=context,
                static_dir="",
                auto_style=True,
                marker=component.get("marker", "content"),
                content=component.get("content", ""),
                frontmatte=component.get("frontmatter", {})
            )
    except Exception as e:
        raise MockErr(e)

@typed
def preview(component: COMPONENT) -> Nill:
    try:
        html = render(style(mock(component)))
        temp_file = cmd.mktemp.file(extension="html")
        file.write(
            filepath=temp_file,
            content=html
        )
        webbrowser.open_new_tab(f'file://{path.abs(temp_file)}')
        cmd.rm(temp_file)
    except Exception as e:
        raise PreviewErr(e)
