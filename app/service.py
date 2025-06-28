import re
import functools
from inspect import signature
from typed import typed, Union, Str
from utils import md
from jinja2 import Environment, DictLoader, StrictUndefined
from bs4 import BeautifulSoup, Tag
from app.mods.helper import _jinja_regex
from app.err import RenderErr, BuildErr
from app.mods.types import Component, Jinja, Static, Page, StaticPage

@typed
def render(component: Component) -> Str:
    try:
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
        if not isinstance(template_block_string, Jinja):
            raise TypeError("Invalid value returned by definer function (not Jinja).")

        regex_str = re.compile(_jinja_regex(), re.DOTALL)
        match = regex_str.match(template_block_string)
        if not match:
            raise TypeError("Invalid Jinja block string format.")
        jinja_content = match.group(1)
        template_name = getattr(definer, '__name__', 'template')

        dep_context = {}

        def make_rendered_dep_func(dep):
            def _inner(*args, **kwargs):
                from inspect import signature
                sig = signature(dep)
                param_names = [p.name for p in sig.parameters.values()]
                child_context = dict(context)
                for i, value in enumerate(args):
                    if i < len(param_names):
                        child_context[param_names[i]] = value
                child_context.update(kwargs)
                dep_args = {k: v for k, v in child_context.items() if k in param_names}
                dep_template_str = dep(**dep_args)
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
    except Exception as e:
        raise RenderErr(e)

@typed
def build(static: Static) -> Component:
    try:
        definer = static.get('definer')
        marker = static.get('marker', 'content')
        content = static.get('content', '')
        html = md.to_html(content)
        typed_func = getattr(definer, 'func', definer)
        import inspect
        sig = inspect.signature(typed_func)
        call_args = {}
        for param in sig.parameters.values():
            if param.name == 'depends_on':
                continue
            if param.default is param.empty:
                ctx = static.get('context', {})
                call_args[param.name] = ctx.get(param.name, '')
            else:
                ctx = static.get('context', {})
                if param.name in ctx:
                    call_args[param.name] = ctx[param.name]

        template_block_string = definer(**call_args)

        from app.mods.helper import _jinja_regex

        regex_str = re.compile(_jinja_regex(), re.DOTALL)
        match = regex_str.match(template_block_string)
        if not match:
            raise TypeError("Invalid Jinja block string format when building static.")

        jinja_content = match.group(1)
        marker_regex = r"\{\{\s*"+re.escape(marker)+r"\s*\}\}"

        new_jinja_content = re.sub(marker_regex, str(html), jinja_content, count=1)

        @typed
        def new_definer() -> Jinja:
            return f"jinja\n{new_jinja_content}"

        context = static.get('context', {}).copy()
        context.update({'frontmatter': static.get('frontmatter', {})})

        component = {
            'definer': new_definer,
            'context': context
        }
        return component
    except Exception as e:
        raise BuildErr(e)

@typed
def style(page: Union(Page, StaticPage)) -> Union(Page, StaticPage):
    if not page.get("auto_style", False):
        return page

    current_page = page
    if isinstance(page, StaticPage):
        from app.service import build
        component_to_render = build(page)
    else:
        component_to_render = page

    html_content = render(component_to_render)
    soup = BeautifulSoup(html_content, 'html.parser')

    def escape_class_selector(cls):
        return cls.replace(':', '\\:').replace('#', '\\#').replace('[', '\\[').replace(']', '\\]').replace('.', '\\.')

    PREFIXES_MAP = {
        "phone":   "(min-width: 0px) and (max-width: 767px)",
        "tablet":  "(min-width: 768px) and (max-width: 1024px)",
        "mobile":  "(min-width: 0px) and (max-width: 1024px)", # phone or tablet
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
    NOT_FLAG = "not" # Canonical name for 'not'
    NOT_ALIASES = ["n"] # Just 'n'

    found_styles = {} # e.g., {(media_prefix, is_important, is_not), 'mt-10px': 'margin-top: 10px;'}

    patterns = {
        'margin_padding': re.compile(r'(m[tblr]|p[tblr])-(\d+(?:\.\d+)?)(px|vh|vw|em|rem|%)'),
        'border': re.compile(r'b(t|b|r|l)-(\d+(?:\.\d+)?)(px|em|rem|%)?-(\w+)'), # bt-1px-solid, btl-2px-dashed
        'font_size': re.compile(r'fz-(\d+(?:\.\d+)?)(px|em|rem|%)'),
        'font_weight': re.compile(r'fw-(extra-light|el|light|l|normal|n|bold|b|extra-bold|eb|black|B|\d{3})'),
        'font_family': re.compile(r'ff-\[(.+?)\]'), # ff-[Roboto Mono, monospace]
        'font_style': re.compile(r'fs-(italic|it|normal|oblique)'),
        'text_decoration': re.compile(r'td-(underline|u|overline|o|line-through|lt|none)'),
        'letter_spacing': re.compile(r'ls-(\d+(?:\.\d+)?)(em|px|rem|%)'),
        'color_hex_rgb': re.compile(r'fc-\[(#([0-9a-fA-F]{3}){1,2}|rgb\((\d{1,3},\s*\d{1,3},\s*\d{1,3})\))\]'),
        'color_var': re.compile(r'fc-([a-zA-Z][a-zA-Z0-9_\-]+)'),
        'text_transform': re.compile(r'tt-(cap|up|upper|lw|low|lower)'), # text-transform
        'width': re.compile(r'w-(full|auto|none|\d+(?:\.\d+)?(?:px|%|vw|vh|em|rem))'), # width
        'height': re.compile(r'h-(full|auto|none|\d+(?:\.\d+)?(?:px|%|vw|vh|em|rem))'), # height
        'min_width': re.compile(r'mw-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'), # min-width
        'max_width': re.compile(r'Mw-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'), # max-width
        'min_height': re.compile(r'mh-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'), # min-height
        'max_height': re.compile(r'Mh-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'), # max-height
        'gap': re.compile(r'gap-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'), # gap
        'border_radius': re.compile(r'(radius|bR)-(\d+(?:\.\d+)?)(px|%|em|rem)'), # border-radius
        'z_index': re.compile(r'z-(full|none|\d+)'), # z-index

        'background_color_hex_rgb': re.compile(r'bg-\[(#([0-9a-fA-F]{3}){1,2}|rgb\((\d{1,3},\s*\d{1,3},\s*\d{1,3})\))\]'),
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
    new_css_rules_list.extend(css_buckets[None][True][False]) # Important global rules
    for canonical_media_name in CANONICAL_MEDIA_NAMES:
        mq_expression = PREFIXES_MAP[canonical_media_name] # e.g., "(min-width: 0px) and (max-width: 767px)"

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
            if canonical_media_name == "phone": # (0px - 767px)
                not_mq_expression = "(min-width: 768px)"
            elif canonical_media_name == "tablet": # (768px - 1024px)
                not_mq_expression = "(max-width: 767px), (min-width: 1025px)"
            elif canonical_media_name == "mobile": # (0px - 1024px) -> Inverse is anything > 1024px
                not_mq_expression = "(min-width: 1025px)"
            elif canonical_media_name == "desktop": # (1025px - 10000px) -> Inverse is anything <= 1024px
                not_mq_expression = "(max-width: 1024px)" # This covers 0px to 1024px

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

    def new_definer_func() -> Jinja:
        return final_jinja_str

    if hasattr(original_definer, '__name__'):
        new_definer_func.__name__ = original_definer.__name__ + "_styled"
    if hasattr(original_definer, '__annotations__'):
        new_definer_func.__annotations__ = original_definer.__annotations__

    from typed import typed # This line was original, keeping it.
    styled_definer = typed(new_definer_func)
    return page.__class__({**page, "definer": styled_definer}) 
