import re
import threading
import webbrowser
import time
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from socketserver import ThreadingMixIn
from inspect import signature, Parameter, getsourcefile
from jinja2 import Environment, DictLoader, StrictUndefined, meta
from typed import typed, Dict, Any, Str, List
from app.mods.helper.types import COMPONENT
from bs4 import BeautifulSoup, NavigableString
from app.err import StyleErr, MinifyErr, PreviewErr


@typed
def _responsive(html: Str) -> Str:
    _blocks = [
        ("desktop",      "(min-width: 1024px)"),
        ("tablet",       "(min-width: 640px) and (max-width: 1023px)"),
        ("phone",        "(max-width: 639px)"),
        ("mobile",       "(max-width: 1023px)"),
        ("not-desktop",  "(max-width: 1023px)"),
        ("not-tablet",   "(max-width: 639px), (min-width: 1024px)"),
        ("not-phone",    "(min-width: 640px)"),
        ("not-mobile",   "(min-width: 1024px)"),
    ]
    tag_css = []
    seen = set()
    for tag, media in _blocks:
        pat = r"<{0}[\s>]".format(tag.replace("-", "[-]?"))
        if re.search(pat, html):
            if tag not in seen:
                seen.add(tag)
                base = tag
                tag1 = tag.replace("-", "")
                tag_css.append(f"{base} "+"{ display: none; }")
                tag_css.append(f"@media {media} "+"{ "+f"{base} "+"{ display: inline; }"+" }")
    if tag_css:
        style_tag = "<style>" + "\n".join(tag_css) + "</style>"
        m = re.search(r"<head[^>]*>", html, re.IGNORECASE)
        if m:
            html = html[:m.end()] + style_tag + html[m.end():]
        else:
            html = style_tag + html
    return html

@typed
def _style(html: Str) -> Str:
    try:
        soup = BeautifulSoup(html, 'html.parser')

        def escape_class_selector(cls):
            return (cls.replace(':', '\\:')
                        .replace('#', '\\#')
                        .replace('[', '\\[')
                        .replace(']', '\\]')
                        .replace('.', '\\.')
                    )

        MEDIA_PREFIXES = {
            "phone": "(min-width: 0px) and (max-width: 767px)",
            "tablet": "(min-width: 768px) and (max-width: 1024px)",
            "mobile": "(min-width: 0px) and (max-width: 1024px)",
            "desktop": "(min-width: 1025px) and (max-width: 10000px)",
        }
        MEDIA_ALIASES = {
            "p": "phone", "ph": "phone",
            "t": "tablet", "tab": "tablet",
            "m": "mobile", "mob": "mobile",
            "d": "desktop", "desk": "desktop", "dsk": "desktop",
        }

        PSEUDO_PREFIXES = {
            "hover": "hover",
            "h": "hover",
            "active": "active",
            "a": "active",
            "focus": "focus",
            "f": "focus",
        }
        PSEUDO_ORDER = ["hover", "active", "focus"]

        IMPORTANT_PREFIXES = {"!", "i", "important", "imp"}
        NOT_PREFIXES = {"not", "n"}

        MEDIA_ALL = set(MEDIA_PREFIXES.keys()) | set(MEDIA_ALIASES.keys())
        PSEUDO_ALL = set(PSEUDO_PREFIXES.keys())
        IMP_ALL = IMPORTANT_PREFIXES
        NOT_ALL = NOT_PREFIXES

        patterns = {
            'margin_padding': re.compile(r'(m[tblr]|p[tblr])-(\d+(?:\.\d+)?)(px|vh|vw|em|rem|%)'),
            'border': re.compile(r'b(t|b|r|l)-(\d+(?:\.\d+)?)(px|em|rem|%)?-(\w+)'),
            'font_size': re.compile(r'f[sz]-(\d+(?:\.\d+)?)(px|em|rem|%)'),
            'font_weight': re.compile(r'fw-(extra-light|el|light|l|normal|n|bold|b|extra-bold|eb|black|B|\d{3})'),
            'font_family': re.compile(r'ff-\[(.+?)\]'),
            'font_style': re.compile(r'fs-(italic|it|normal|oblique)'),
            'text_decoration': re.compile(r'td-(underline|u|overline|o|line-through|lt|none)'),
            'letter_spacing': re.compile(r'ls-(\d+(?:\.\d+)?)(em|px|rem|%)'),
            'color_hex_rgb': re.compile(r'fc-(#([0-9a-fA-F]{3}){1,2}|rgb\((?:\d{1,3},\d{1,3},\d{1,3})\))'),
            'color_var': re.compile(r'fc-([a-zA-Z][a-zA-Z0-9_\-]+)'),
            'fill_hex_rgb': re.compile(r'fill-(#([0-9a-fA-F]{3}){1,2}|rgb\((?:\d{1,3},\d{1,3},\d{1,3})\))'),
            'fill_var': re.compile(r'fill-([a-zA-Z][a-zA-Z0-9_\-]+)'),
            'text_transform': re.compile(r'tt-(cap|up|upper|lw|low|lower)'),
            'width': re.compile(r'w-(full|auto|none|\d+(?:\.\d+)?(?:px|%|vw|vh|em|rem))'),
            'height': re.compile(r'h-(full|auto|none|\d+(?:\.\d+)?(?:px|%|vw|vh|em|rem))'),
            'min_width': re.compile(r'mw-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'),
            'max_width': re.compile(r'Mw-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'),
            'min_height': re.compile(r'mh-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'),
            'max_height': re.compile(r'Mh-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'),
            'gap': re.compile(r'gap-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'),
            'border_radius': re.compile(r'(radius|bR)-(\d+(?:\.\d+)?)(px|%|em|rem)'),
            'z_index': re.compile(r'z-(full|none|\d+)'),
            'background_color_hex_rgb': re.compile(r'bg-(#([0-9a-fA-F]{3}){1,2}|rgb\((?:\d{1,3},\s*\d{1,3},\s*\d{1,3})\))'),
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
            'padding_margin': re.compile(r'(p|m)-(\d+(?:\.\d+)?)(px|vh|vw|em|rem|%)'),
            'margin_padding': re.compile(r'(m[tblr]|p[tblr])-(\d+(?:\.\d+)?)(px|vh|vw|em|rem|%)')
        }

        style_property_map = {
            'p': 'padding',
            'm': 'margin',
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
            match = patterns['padding_margin'].match(class_name)
            if match:
                prefix, value, unit = match.groups()
                prop = style_property_map[prefix]
                css_rule = f"{prop}: {value}{unit};"
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
                    unit = unit if unit else 'px'
                    css_rule = f"{prop}: {value}{unit} {color_or_style};"
            if not css_rule:
                match = patterns['font_size'].match(class_name)
                if match:
                    value, unit = match.groups()
                    css_rule = f"font-size: {value}{unit};"
            if not css_rule:
                match = patterns['font_weight'].match(class_name)
                if match:
                    weight_key = match.group(1)
                    weight_val = font_weight_map.get(weight_key)
                    if weight_val is None:
                        try:
                            weight_val = int(weight_key)
                        except ValueError:
                            weight_val = weight_key
                    css_rule = f"font-weight: {weight_val};"
            if not css_rule:
                match = patterns['font_family'].match(class_name)
                if match:
                    font_families_encoded = match.group(1)
                    font_families_decoded = font_families_encoded.replace('_', ' ')
                    css_rule = f"font-family: {font_families_decoded};"
            if not css_rule:
                match = patterns['font_style'].match(class_name)
                if match:
                    style_key = match.group(1)
                    style_val = font_style_map.get(style_key, style_key)
                    css_rule = f"font-style: {style_val};"
            if not css_rule:
                match = patterns['text_decoration'].match(class_name)
                if match:
                    decoration_key = match.group(1)
                    decoration_val = text_decoration_map.get(decoration_key, decoration_key)
                    css_rule = f"text-decoration: {decoration_val};"
            if not css_rule:
                match = patterns['letter_spacing'].match(class_name)
                if match:
                    value, unit = match.groups()
                    css_rule = f"letter-spacing: {value}{unit};"
            if not css_rule:
                match = patterns['color_hex_rgb'].match(class_name)
                if match:
                    color_val = match.group(1)
                    css_rule = f"color: {color_val};"
            if not css_rule:
                match = patterns['color_var'].match(class_name)
                if match:
                    var_name = match.group(1).replace('-', '_')
                    css_rule = f"color: var(--{var_name});"
            if not css_rule:
                match = patterns['fill_hex_rgb'].match(class_name)
                if match:
                    color_val = match.group(1)
                    css_rule = f"fill: {color_val};"
            if not css_rule:
                match = patterns['fill_var'].match(class_name)
                if match:
                    var_name = match.group(1).replace('-', '_')
                    css_rule = f"fill: var(--{var_name});"
            if not css_rule:
                match = patterns['text_transform'].match(class_name)
                if match:
                    transform_key = match.group(1)
                    transform_val = text_transform_map.get(transform_key)
                    css_rule = f"text-transform: {transform_val};"
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
                    css_rule = f"width: {css_val};"
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
                    css_rule = f"height: {css_val};"
            if not css_rule:
                match = patterns['min_width'].match(class_name)
                if match:
                    value, unit = match.groups()
                    css_rule = f"min-width: {value}{unit};"
            if not css_rule:
                match = patterns['max_width'].match(class_name)
                if match:
                    value, unit = match.groups()
                    css_rule = f"max-width: {value}{unit};"
            if not css_rule:
                match = patterns['min_height'].match(class_name)
                if match:
                    value, unit = match.groups()
                    css_rule = f"min-height: {value}{unit};"
            if not css_rule:
                match = patterns['max_height'].match(class_name)
                if match:
                    value, unit = match.groups()
                    css_rule = f"max-height: {value}{unit};"
            if not css_rule:
                match = patterns['gap'].match(class_name)
                if match:
                    value, unit = match.groups()
                    css_rule = f"gap: {value}{unit};"
            if not css_rule:
                match = patterns['border_radius'].match(class_name)
                if match:
                    prefix, value, unit = match.groups()
                    css_rule = f"border-radius: {value}{unit};"
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
                    css_rule = f"z-index: {css_val};"
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

        def parse_prefixed_class(class_name: str):
            """Parse aliases and collect flags. Return error if any illegal usage."""
            parts = class_name.split(':')
            original = class_name
            error = None
            found_media = None
            found_pseudos = []
            found_important = False
            found_not = False
            i = 0
            while i < len(parts):
                part = parts[i]
                lpart = part.lower()
                if lpart in NOT_ALL:
                    if i != 0:
                        error = f"ERROR({original})"
                        return {'error': error}
                    if i+1 >= len(parts):
                        error = f"ERROR({original})"
                        return {'error': error}
                    if parts[i+1].lower() not in MEDIA_ALL:
                        error = f"ERROR({original})"
                        return {'error': error}
                    found_not = True
                    i += 1
                elif lpart in IMP_ALL:
                    found_important = True
                    i += 1
                elif lpart in MEDIA_ALL:
                    if found_media is not None:
                        error = f"ERROR({original})"
                        return {'error': error}
                    media = MEDIA_ALIASES.get(lpart, lpart)
                    found_media = media
                    i += 1
                elif lpart in PSEUDO_ALL:
                    pseudo = PSEUDO_PREFIXES[lpart]
                    if pseudo in found_pseudos:
                        # duplicate pseudo
                        error = f"ERROR({original})"
                        return {'error': error}
                    found_pseudos.append(pseudo)
                    i += 1
                else:
                    break
            base = ":".join(parts[i:])
            if found_not:
                if not found_media or found_pseudos:
                    error = f"ERROR({original})"
                    return {'error': error}

            for j, part in enumerate(parts):
                if part.lower() in NOT_ALL and j != 0:
                    error = f"ERROR({original})"
                    return {'error': error}
            if not base:
                error = f"ERROR({original})"
                return {'error': error}
            pseudos_sorted = sorted(found_pseudos, key=lambda p: PSEUDO_ORDER.index(p)) if found_pseudos else []
            return {
                'error': None,
                'important': found_important,
                'media': found_media,
                'pseudos': pseudos_sorted,
                'not': found_not,
                'base': base,
                'original': class_name
            }

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

        bucket_not_media = {
            "phone": "(min-width: 768px)",
            "tablet": "(max-width: 767px), (min-width: 1025px)",
            "mobile": "(min-width: 1025px)",
            "desktop": "(max-width: 1024px)",
        }

        css_rules_errors = []

        for tag in soup.find_all(True):
            if tag.has_attr('class'):
                for class_name in tag['class']:
                    pref = parse_prefixed_class(class_name)
                    if pref['error']:
                        css_rules_errors.append(f".{escape_class_selector(class_name)} {{ color: red; font-weight: bold; content: '{pref['error']}'; }}")
                        continue

                    base_rule = style_for_base_class(pref['base'])
                    if not base_rule:
                        continue
                    selector = '.' + escape_class_selector(pref['original'])
                    for pseudo in pref['pseudos']:
                        selector += f":{pseudo}"

                    rule_content = base_rule.strip()
                    if pref['important']:
                        rule_content = re.sub(r'(?<!important)\s*;', ' !important;', rule_content)

                    rule_str = f"{selector} {{\n    {rule_content}\n}}"

                    if pref['not']:
                        canonical_media = pref['media'] if pref['media'] in CANONICAL_MEDIA_NAMES else None
                        css_buckets[canonical_media][pref['important']][True].append(rule_str)
                    elif pref['media']:
                        canonical_media = pref['media'] if pref['media'] in CANONICAL_MEDIA_NAMES else pref['media']
                        if canonical_media not in css_buckets:
                            css_buckets[None][pref['important']][False].append(rule_str)
                        else:
                            css_buckets[canonical_media][pref['important']][False].append(rule_str)
                    else:
                        css_buckets[None][pref['important']][False].append(rule_str)

        new_css_rules_list = []

        new_css_rules_list.extend(css_buckets[None][False][False])
        new_css_rules_list.extend(css_buckets[None][True][False])
        for canonical_media_name in CANONICAL_MEDIA_NAMES:
            mq_expression = MEDIA_PREFIXES[canonical_media_name]
            rules_for_this_mq = []
            rules_for_this_mq.extend(css_buckets[canonical_media_name][False][False])
            rules_for_this_mq.extend(css_buckets[canonical_media_name][True][False])
            if rules_for_this_mq:
                new_css_rules_list.append(f"@media {mq_expression} {{\n{chr(10).join(rules_for_this_mq)}\n}}\n")
            not_rules_for_this_mq = []
            not_rules_for_this_mq.extend(css_buckets[canonical_media_name][False][True])
            not_rules_for_this_mq.extend(css_buckets[canonical_media_name][True][True])
            if not_rules_for_this_mq:
                not_mq_expression = bucket_not_media[canonical_media_name]
                new_css_rules_list.append(f"@media {not_mq_expression} {{\n{chr(10).join(not_rules_for_this_mq)}\n}}\n")

        if css_rules_errors:
            new_css_rules_list.append('\n'.join(css_rules_errors))

        new_css_rules = "\n".join(new_css_rules_list)
        if new_css_rules:
            head_tag = soup.find('head')
            if head_tag:
                style_tag = soup.head.find('style')
                if style_tag:
                    if style_tag.string:
                        style_tag.string += "\n" + new_css_rules
                    else:
                        style_tag.string = new_css_rules
                else:
                    new_style_tag = soup.new_tag("style")
                    new_style_tag.string = new_css_rules
                    soup.head.append(new_style_tag)
                    new_style_tag.insert_after(NavigableString("\n"))
                return str(soup)
            else:
                new_style_tag = soup.new_tag("style")
                new_style_tag.string = new_css_rules
                if soup.contents:
                    soup.insert(0, new_style_tag)
                    new_style_tag.insert_after(NavigableString("\n"))
                else:
                    soup.append(new_style_tag)
                    soup.append(NavigableString("\n"))
                return str(soup)
        else:
            return str(soup)
    except Exception as e:
        raise StyleErr(e)

def _minify(html: str) -> str:
    """
    Minifies HTML string including inline CSS and JavaScript.
    """
    def minify_js(match):
        open_tag = match.group(1)
        js_code = match.group(2)
        if 'src=' in open_tag.lower():
            return match.group(0)
        js_code = re.sub(r'//.*|/\*[\s\S]*?\*/', '', js_code)
        js_code = re.sub(r'\s+', ' ', js_code)
        js_code = re.sub(r'\s*([{}();,:])\s*', r'\1', js_code)
        return f"{open_tag}{js_code.strip()}</script>"

    html = re.sub(
        r'(<script\b[^>]*>)(.*?)(</script>)',
        minify_js,
        html,
        flags=re.DOTALL | re.IGNORECASE
    )

    def minify_css(match):
        open_tag = match.group(1)
        css_code = match.group(2)
        if 'href=' in open_tag.lower() or 'src=' in open_tag.lower():
            return match.group(0)
        css_code = re.sub(r'/\*[\s\S]*?\*/', '', css_code)
        css_code = re.sub(r'\s+', ' ', css_code)
        css_code = re.sub(r'\s*([{}:;,])\s*', r'\1', css_code)
        return f"{open_tag}{css_code.strip()}</style>"

    html = re.sub(
        r'(<style\b[^>]*>)(.*?)(</style>)',
        minify_css,
        html,
        flags=re.DOTALL | re.IGNORECASE
    )

    def minify_inline_style(match):
        quote = match.group(1)
        css_code = match.group(2)
        css_code = re.sub(r'/\*[\s\S]*?\*/', '', css_code)
        css_code = re.sub(r'\s+', ' ', css_code)
        css_code = re.sub(r'\s*([{}:;,])\s*', r'\1', css_code)
        return f'style={quote}{css_code.strip()}{quote}'

    html = re.sub(
        r'style=([\'"])(.*?)(\1)',
        minify_inline_style,
        html,
        flags=re.DOTALL | re.IGNORECASE
    )

    html = re.sub(r'<!--(?!\[if)[\s\S]*?-->', '', html)
    html = re.sub(r'>\s+<', '><', html)
    html = re.sub(r'\s{2,}', ' ', html)
    html = re.sub(r'[\n\t\r]', '', html)
    html = re.sub(r'>\s+', '>', html)
    html = re.sub(r'\s+<', '<', html)
    html = html.strip()
    return html

class _PREVIEW:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(_PREVIEW, cls).__new__(cls)
            cls._instance._init_singleton()
        return cls._instance

    def _init_singleton(self):
        self.stack = []
        self.server_thread = None
        self.has_started = False
        self.port = 4955
        self.file_dependents = {}
        self.source_cache = {}
        self.reload_ts = str(time.time())
        self.single_preview = None
        self.lock = threading.Lock()
        self._reloader_thread = None
        self._browser_opened = False

    def _add(self, comp: COMPONENT, __name__=None, __scripts__=None, __assets__=None, __responsive__=True, **kwargs):
        """
        Adds a component to the preview stack.
        Can optionally accept a __name__ for the component instance, and lists of __scripts__ and __assets__.
        """
        with self.lock:
            self.stack.append((comp, kwargs, __scripts__ or [], __assets__ or [], __responsive__ or True, __name__))
            self._update_watch(comp)
            for scr in (__scripts__ or []):
                if scr.script_src and not scr.script_src.startswith(('http://', 'https://')):
                    self._update_watch(scr.script_src)
            for asset in (__assets__ or []):
                if asset.asset_href and not asset.asset_href.startswith(('http://', 'https://')):
                    self._update_watch(asset.asset_href)
            self._touch_reload()

    def _rm(self, identifier):
        """
        Removes components from the preview stack.
        If `identifier` is a component function, removes all instances of that component.
        If `identifier` is a string, removes the instance with the matching __name__.
        """
        with self.lock:
            if isinstance(identifier, str):
                new_stack = []
                removed = False
                for item_comp, item_kwargs, item_scripts, item_assets, item_name in self.stack:
                    if item_name == identifier:
                        removed = True
                        if item_comp in self.file_dependents:
                            other_instances = [x for x in new_stack if x[0] is item_comp]
                            if not other_instances:
                                del self.file_dependents[item_comp]
                    else:
                        new_stack.append((item_comp, item_kwargs, item_scripts, item_assets, item_name))
                if removed:
                    self.stack = new_stack
                    self._touch_reload()
            else:
                new_stack = [item for item in self.stack if item[0] is not identifier]
                if len(new_stack) < len(self.stack):
                    self.stack = new_stack
                    if identifier in self.file_dependents:
                        del self.file_dependents[identifier]
                    self._touch_reload()

    def _clean(self):
        """Removes all components from the preview stack."""
        with self.lock:
            self.stack.clear()
            self.file_dependents = {}
            self._touch_reload()

    def _run(self, autoload=True):
        if os.environ.get("APP_PREVIEW_BROWSER_OPENED") == '1':
            self._browser_opened = True
        if autoload and os.environ.get("APP_PREVIEW_CHILD") != "1":
            if 'APP_PREVIEW_BROWSER_OPENED' in os.environ:
                del os.environ['APP_PREVIEW_BROWSER_OPENED']
            import subprocess
            args = [sys.executable] + sys.argv
            env = dict(os.environ)
            env["APP_PREVIEW_CHILD"] = "1"
            print("[app-preview] Autoreloading enabled (CTRL+C to stop)")
            p = subprocess.Popen(args, env=env)
            try:
                p.wait()
            except KeyboardInterrupt:
                print("Preview stopped by user.")
                p.terminate()
                p.wait()
            sys.exit(0)

        self.has_started = True
        self._reloader_thread = threading.Thread(target=self._watchdog_restart, daemon=True)
        try:
            main_script_path = os.path.abspath(sys.argv[0])
            self._update_watch(main_script_path)

            for comp, _, scripts, assets, _ in self.stack:
                self._update_watch(comp)
                for scr in scripts:
                    if scr.script_src and not scr.script_src.startswith(('http://', 'https://')):
                        self._update_watch(scr.script_src)
                for asset in assets:
                    if asset.asset_href and not asset.asset_href.startswith(('http://', 'https://')):
                        self._update_watch(asset.asset_href)

        except Exception as e:
            print(f"DEBUG: Initial script/component/asset watch failed: {e}")
        self._reloader_thread.start()
        self._serve_forever()

    def __call__(self, comp=None, __scripts__=None, __assets__=None, __responsive__=True, **kwargs):
        if comp:
            with self.lock:
                self._clean()
                self._add(comp, __scripts=__scripts__, __assets=__assets__, __responsive__=__responsive__, **kwargs)
            self._run()
        else:
            self._run()


    def _serve_forever(self):
        Handler = self._make_handler()
        class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
            daemon_threads = True
        httpd = ThreadedHTTPServer(('', self.port), Handler)
        print(f"Preview server running at http://127.0.0.1:{self.port}/ (CTRL+C to stop)")
        if not self._browser_opened:
            try:
                webbrowser.open(f"http://127.0.0.1:{self.port}/")
                self._browser_opened = True
            except Exception:
                pass
        else:
            print("[app-preview] Reloading in existing browser tab (if open)...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Exiting preview server")
            sys.exit(0)

    def _make_handler(self):
        preview_mgr = self
        class PreviewHandler(BaseHTTPRequestHandler):
            def _send(self, data, code=200):
                self.send_response(code)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(data.encode("utf-8"))

            def do_GET(self):
                if self.path.startswith("/__reload_check"):
                    self._send(preview_mgr.reload_ts)
                elif self.path == "/" or self.path.startswith("/?"):
                    html = preview_mgr._render_page()
                    self._send(html)
                else:
                    self._send("<h1>Not Found</h1>", 404)

            def log_message(self, fmt, *args):
                pass
        return PreviewHandler

    def _render_comps(self):
        from app.mods.service import render
        html_parts = []
        for idx, (comp, kwargs, scripts, assets, responsive, _) in enumerate(self.stack):
            rendered = render(comp, __scripts__=scripts, __assets__=assets, __responsive__=responsive, **kwargs)
            html_parts.append(f'<div>{rendered}</div>')
            if idx < len(self.stack) - 1:
                html_parts.append("""
<div style="width:100%;margin:20px 0 20px 0;text-align:center;">
    <hr style="margin-top:10px;margin-bottom:10px;width:100%;border:3px solid #000000;"/>
</div>
""")
        return "\n".join(html_parts)

    def _generate_page(self, content):
        js = f"""
<script>
(function(){{
    let last="{self.reload_ts}";
    setInterval(function(){{
        fetch("/__reload_check").then(r=>r.text()).then(txt=>{{if(txt!==last)location.reload();}});
    }}, 999);
}})();
</script>
"""
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Component Preview</title>
    <meta charset="utf-8">
    {js}
</head>
<body>
{content}
</body>
</html>
"""
    def _render_page(self):
        html = self._render_comps()
        return self._generate_page(html)

    def _update_watch(self, obj):
        src = None
        try:
            if callable(obj):
                actual_obj_for_source = getattr(obj, "func", obj)
                src = sys.modules[actual_obj_for_source.__module__].__file__
                if not src:
                    src = getattr(actual_obj_for_source, '__file__', None)
                if not src:
                    try:
                        src = getsourcefile(actual_obj_for_source)
                    except TypeError:
                        pass
            elif isinstance(obj, str) and os.path.isfile(obj):
                src = obj
            else:
                return
        except Exception as e:
            pass
        if src:
            src = os.path.abspath(src)
            key = obj if not isinstance(obj, str) else src
            if key not in self.file_dependents:
                self.file_dependents[key] = set()
            self.file_dependents[key].add(src)
            try:
                self.source_cache[src] = os.path.getmtime(src)
            except FileNotFoundError:
                pass
        else:
            pass

    def _touch_reload(self):
        self.reload_ts = str(time.time())

    def _watchdog_restart(self):
        """Restart process if dependencies have changed."""
        time.sleep(0.5)
        while True:
            changed = False
            watched_files = set()
            with self.lock:
                for srcs_set in self.file_dependents.values():
                    watched_files.update(srcs_set)

            if not watched_files:
                pass

            for f in watched_files:
                try:
                    current_mtime = os.path.getmtime(f)
                    cached_mtime = self.source_cache.get(f)
                    if cached_mtime is not None and current_mtime != cached_mtime:
                        print(f"[app-preview] Detected change in {f}, restarting...")
                        self.source_cache[f] = current_mtime
                        changed = True
                        break
                except FileNotFoundError:
                    print(f"[app-preview] Detected missing file {f}, restarting...")
                    changed = True
                    break
                except Exception as e:
                    print(f"[app-preview] Error watching file {f}: {e}")
                    pass

            if changed:
                os.environ['APP_PREVIEW_BROWSER_OPENED'] = '1'
                os.execv(sys.executable, [sys.executable] + sys.argv)
            time.sleep(1.0)

class _Preview:
    def add(self, comp, __name__=None, __scripts__=None, __assets__=None, __responsive__=True, **kwargs):
        try:
            _PREVIEW()._add(comp, __name__=__name__, __scripts__=__scripts__, __assets__=__assets__, __responsive__=__responsive__, **kwargs)
        except Exception as e:
            raise PreviewErr(e)

    def rm(self, identifier):
        try:
            _PREVIEW()._rm(identifier)
        except Exception as e:
            raise PreviewErr(e)

    def clean(self):
        try:
            _PREVIEW()._clean()
        except Exception as e:
            raise PreviewErr(e)

    def run(self, autoload=True):
        try:
            _PREVIEW()._run(autoload)
        except Exception as e:
            raise PreviewErr(e)
