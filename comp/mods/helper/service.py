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
from comp.mods.helper.types import COMPONENT
from bs4 import BeautifulSoup, NavigableString
from comp.mods.err import StyleErr, MinifyErr, PreviewErr


def _style(html: str) -> str:
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
            "hover": "hover", "h": "hover",
            "active": "active", "a": "active",
            "focus": "focus", "f": "focus",
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
            'border':         re.compile(r'b(t|b|r|l)-(\d+(?:\.\d+)?)(px|em|rem|%)?-(\w+)'),
            'font_size':      re.compile(r'f[sz]-(\d+(?:\.\d+)?)(px|em|rem|%)'),
            'font_weight':    re.compile(r'fw-(extra-light|el|light|l|normal|n|bold|b|extra-bold|eb|black|B|\d{3})'),
            'font_family':    re.compile(r'ff-\[(.+?)\]'),
            'font_style':     re.compile(r'fs-(italic|it|normal|oblique)'),
            'text_decoration':re.compile(r'td-(underline|u|overline|o|line-through|lt|none)'),
            'letter_spacing': re.compile(r'ls-(\d+(?:\.\d+)?)(em|px|rem|%)'),
            'color_hex_rgb':  re.compile(r'fc-(#([0-9a-fA-F]{3}){1,2}|rgb\((?:\d{1,3},\d{1,3},\d{1,3})\))'),
            'color_var':      re.compile(r'fc-([a-zA-Z][a-zA-Z0-9_\-]+)'),
            'fill_hex_rgb':   re.compile(r'fill-(#([0-9a-fA-F]{3}){1,2}|rgb\((?:\d{1,3},\d{1,3},\d{1,3})\))'),
            'fill_var':       re.compile(r'fill-([a-zA-Z][a-zA-Z0-9_\-]+)'),
            'text_transform': re.compile(r'tt-(cap|up|upper|lw|low|lower)'),
            'width':          re.compile(r'w-(full|auto|none|\d+(?:\.\d+)?(?:px|%|vw|vh|em|rem))'),
            'height':         re.compile(r'h-(full|auto|none|\d+(?:\.\d+)?(?:px|%|vw|vh|em|rem))'),
            'min_width':      re.compile(r'mw-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'),
            'max_width':      re.compile(r'Mw-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'),
            'min_height':     re.compile(r'mh-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'),
            'max_height':     re.compile(r'Mh-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'),
            'gap':            re.compile(r'gap-(\d+(?:\.\d+)?)(px|%|vw|vh|em|rem)'),
            'border_radius':  re.compile(r'(radius|bR)-(\d+(?:\.\d+)?)(px|%|em|rem)'),
            'z_index':        re.compile(r'z-(full|none|\d+)'),
            'background_color_hex_rgb':
                              re.compile(r'bg-(#([0-9a-fA-F]{3}){1,2}|rgb\((?:\d{1,3},\s*\d{1,3},\d{1,3})\))'),
            'background_size':re.compile(r'bg-sz-(\d+(?:\.\d+)?)(px|%|em|rem)'),
            'background_blur':re.compile(r'(?:bg-blur|blur)-(\d+(?:\.\d+)?)(px|em|rem|%)'),
            'display':        re.compile(r'^(?:flex|fl|inline|inl|block|blk|table|tab'
                                         r'|inline-block|inl-blk|inline-flex|inl-fl)$'),
            'position':       re.compile(r'pos-(fix|abs|rel|stk)'),
            'text_justify':   re.compile(r'(?:just|jst)-(start|st|end|ed|left|lft|right|rgt|center|cnt)'),
            'overflow_x':     re.compile(r'over-x'),
            'overflow_y':     re.compile(r'over-y'),
            'scroll_x':       re.compile(r'(?:scroll|scl)-x'),
            'scroll_y':       re.compile(r'(?:scroll|scl)-y'),
            'scroll_all':     re.compile(r'(?:scroll|scl)$'),
            'padding_margin': re.compile(r'(p|m)-(\d+(?:\.\d+)?)(px|vh|vw|em|rem|%)'),
        }

        style_property_map = {
            'p':'padding','m':'margin',
            'mt':'margin-top','mb':'margin-bottom','ml':'margin-left','mr':'margin-right',
            'pt':'padding-top','pb':'padding-bottom','pl':'padding-left','pr':'padding-right',
            'bt':'border-top','bb':'border-bottom','br':'border-right','bl':'border-left',
            'fz':'font-size','fw':'font-weight','ff':'font-family','fs':'font-style',
            'td':'text-decoration','ls':'letter-spacing','fc':'color','tt':'text-transform',
            'w':'width','h':'height','mw':'min-width','Mw':'max-width',
            'mh':'min-height','Mh':'max-height','gap':'gap',
            'radius':'border-radius','bR':'border-radius',
            'z':'z-index','bg':'background-color','bg-sz':'background-size',
            'bg-blur':'backdrop-filter','fl':'display','inl':'display','blk':'display','tab':'display',
            'inl-blk':'display','inl-fl':'display',
            'pos':'position','just':'text-align','over-x':'overflow-x','over-y':'overflow-y',
            'scroll-x':'position','scroll-y':'position','scroll':'position',
        }

        font_weight_map = {
            'extra-light':200,'el':200,'light':300,'l':300,'normal':400,'n':400,
            'bold':700,'b':700,'extra-bold':800,'eb':800,'black':900,'B':900,
        }
        font_style_map = {'italic':'italic','it':'italic','normal':'normal','oblique':'oblique'}
        text_decoration_map = {'underline':'underline','u':'underline',
                               'overline':'overline','o':'overline',
                               'line-through':'line-through','lt':'line-through','none':'none'}
        text_transform_map = {'cap':'capitalize','up':'uppercase','upper':'uppercase',
                              'lw':'lowercase','low':'lowercase','lower':'lowercase'}
        display_map = {'flex':'flex','fl':'flex','inline':'inline','inl':'inline',
                       'block':'block','blk':'block','table':'table','tab':'table',
                       'inline-block':'inline-block','inl-blk':'inline-block',
                       'inline-flex':'inline-flex','inl-fl':'inline-flex'}
        position_map = {'fix':'fixed','abs':'absolute','rel':'relative','stk':'sticky'}
        text_justify_map = {'start':'start','st':'start','end':'end','ed':'end',
                            'left':'left','lft':'left','right':'right','rgt':'right',
                            'center':'center','cnt':'center'}

        def style_for_base_class(class_name):
            if class_name == "row":
                return "display: flex; flex-wrap: wrap;"
            if class_name == "col":
                return "flex: 1 0 0%;"
            m = re.fullmatch(r"col-(\d+)", class_name)
            if m:
                n = int(m.group(1))
                total = 5
                if 1 <= n <= total:
                    pct = n * 100.0 / total
                    return f"flex: 0 0 {pct:.6f}%; max-width: {pct:.6f}%;"

            css_rule = None
            match = patterns['padding_margin'].match(class_name)
            if match:
                prefix, value, unit = match.groups()
                css_rule = f"{style_property_map[prefix]}: {value}{unit};"
            if not css_rule:
                match = patterns['margin_padding'].match(class_name)
                if match:
                    prefix, value, unit = match.groups()
                    css_rule = f"{style_property_map[prefix]}: {value}{unit};"
            if not css_rule:
                match = patterns['border'].match(class_name)
                if match:
                    t, v, u, style = match.groups()
                    u = u or 'px'
                    css_rule = f"{style_property_map['b'+t]}: {v}{u} {style};"
            if not css_rule:
                match = patterns['font_size'].match(class_name)
                if match:
                    v, u = match.groups()
                    css_rule = f"font-size: {v}{u};"
            if not css_rule:
                match = patterns['font_weight'].match(class_name)
                if match:
                    key = match.group(1)
                    val = font_weight_map.get(key, None)
                    if val is None:
                        try: val = int(key)
                        except: val = key
                    css_rule = f"font-weight: {val};"
            if not css_rule:
                match = patterns['font_family'].match(class_name)
                if match:
                    fam = match.group(1).replace('_',' ')
                    css_rule = f"font-family: {fam};"
            if not css_rule:
                match = patterns['font_style'].match(class_name)
                if match:
                    s = font_style_map.get(match.group(1), match.group(1))
                    css_rule = f"font-style: {s};"
            if not css_rule:
                match = patterns['text_decoration'].match(class_name)
                if match:
                    td = text_decoration_map.get(match.group(1), match.group(1))
                    css_rule = f"text-decoration: {td};"
            if not css_rule:
                match = patterns['letter_spacing'].match(class_name)
                if match:
                    v, u = match.groups()
                    css_rule = f"letter-spacing: {v}{u};"
            if not css_rule:
                match = patterns['color_hex_rgb'].match(class_name)
                if match:
                    css_rule = f"color: {match.group(1)};"
            if not css_rule:
                match = patterns['color_var'].match(class_name)
                if match:
                    var = match.group(1).replace('-','_')
                    css_rule = f"color: var(--{var});"
            if not css_rule:
                match = patterns['fill_hex_rgb'].match(class_name)
                if match:
                    css_rule = f"fill: {match.group(1)};"
            if not css_rule:
                match = patterns['fill_var'].match(class_name)
                if match:
                    var = match.group(1).replace('-','_')
                    css_rule = f"fill: var(--{var});"
            if not css_rule:
                match = patterns['text_transform'].match(class_name)
                if match:
                    tr = text_transform_map.get(match.group(1))
                    css_rule = f"text-transform: {tr};"
            if not css_rule:
                match = patterns['width'].match(class_name)
                if match:
                    w = match.group(1)
                    css_rule = f"width: {'100%' if w=='full' else w+'%' if w.isdigit() else w};"
            if not css_rule:
                match = patterns['height'].match(class_name)
                if match:
                    h = match.group(1)
                    css_rule = f"height: {'100%' if h=='full' else h+'%' if h.isdigit() else h};"
            if not css_rule:
                match = patterns['min_width'].match(class_name)
                if match:
                    v,u = match.groups()
                    css_rule = f"min-width: {v}{u};"
            if not css_rule:
                match = patterns['max_width'].match(class_name)
                if match:
                    v,u = match.groups()
                    css_rule = f"max-width: {v}{u};"
            if not css_rule:
                match = patterns['min_height'].match(class_name)
                if match:
                    v,u = match.groups()
                    css_rule = f"min-height: {v}{u};"
            if not css_rule:
                match = patterns['max_height'].match(class_name)
                if match:
                    v,u = match.groups()
                    css_rule = f"max-height: {v}{u};"
            if not css_rule:
                match = patterns['gap'].match(class_name)
                if match:
                    v,u = match.groups()
                    css_rule = f"gap: {v}{u};"
            if not css_rule:
                match = patterns['border_radius'].match(class_name)
                if match:
                    _,v,u = match.groups()
                    css_rule = f"border-radius: {v}{u};"
            if not css_rule:
                match = patterns['z_index'].match(class_name)
                if match:
                    z = match.group(1)
                    z_val = '100000' if z=='full' else '0' if z=='none' else z
                    css_rule = f"z-index: {z_val};"
            if not css_rule:
                match = patterns['background_color_hex_rgb'].match(class_name)
                if match:
                    css_rule = f"background-color: {match.group(1)};"
            if not css_rule:
                match = patterns['background_size'].match(class_name)
                if match:
                    v,u = match.groups()
                    css_rule = f"background-size: {v}{u};"
            if not css_rule:
                match = patterns['background_blur'].match(class_name)
                if match:
                    v,u = match.groups()
                    css_rule = f"backdrop-filter: blur({v}{u}); background: rgba(0,0,0,0.2);"
            if not css_rule:
                match = patterns['display'].match(class_name)
                if match:
                    dv = display_map.get(class_name)
                    css_rule = f"display: {dv};"
            if not css_rule:
                match = patterns['position'].match(class_name)
                if match:
                    pk = match.group(1)
                    css_rule = f"position: {position_map.get(pk)};"
            if not css_rule:
                match = patterns['text_justify'].match(class_name)
                if match:
                    jk = match.group(1)
                    css_rule = f"text-align: {text_justify_map.get(jk)};"
            if not css_rule:
                if class_name in ['flex-center','fl-cnt','fl-center','flex-cnt']:
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
                    css_rule = "position: fixed; overflow-x: auto; max-height:100vh;"
            if not css_rule:
                match = patterns['scroll_y'].match(class_name)
                if match:
                    css_rule = "position: fixed; overflow-y: auto; max-height:100vh;"
            if not css_rule:
                match = patterns['scroll_all'].match(class_name)
                if match:
                    css_rule = "position: fixed; overflow-x:auto; overflow-y:auto; max-height:100vh;"
            return css_rule

        def parse_prefixed_class(class_name: str):
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
                    if i != 0 or i+1>=len(parts) or parts[i+1].lower() not in MEDIA_ALL:
                        return {'error': f"ERROR({original})"}
                    found_not = True
                    i += 1
                elif lpart in IMP_ALL:
                    found_important = True
                    i += 1
                elif lpart in MEDIA_ALL:
                    if found_media is not None:
                        return {'error': f"ERROR({original})"}
                    found_media = MEDIA_ALIASES.get(lpart, lpart)
                    i += 1
                elif lpart in PSEUDO_ALL:
                    p = PSEUDO_PREFIXES[lpart]
                    if p in found_pseudos:
                        return {'error': f"ERROR({original})"}
                    found_pseudos.append(p)
                    i += 1
                else:
                    break
            base = ":".join(parts[i:])
            if not base:
                return {'error': f"ERROR({original})"}
            pseudos_sorted = sorted(found_pseudos, key=lambda p: PSEUDO_ORDER.index(p))
            return {
                'error': None,
                'important': found_important,
                'media': found_media,
                'pseudos': pseudos_sorted,
                'not': found_not,
                'base': base,
                'original': original
            }

        CANONICAL_MEDIA_NAMES = ["phone","tablet","mobile","desktop"]
        css_rules_parsed = []
        css_rules_errors = []

        for tag in soup.find_all(True):
            if not tag.has_attr('class'):
                continue
            for class_name in tag['class']:
                pref = parse_prefixed_class(class_name)
                if pref['error']:
                    css_rules_errors.append(
                        f".{escape_class_selector(class_name)} {{ color: red; font-weight: bold; content: '{pref['error']}'; }}"
                    )
                    continue

                selector_base = '.' + escape_class_selector(pref['original'])
                if pref['base'] in CANONICAL_MEDIA_NAMES and not pref['not']:
                    css_rules_parsed.append({
                        'selector': selector_base,
                        'rule_content': 'display: none;',
                        'media_query': None,
                        'pseudo_elements': [],
                        'important': False,
                        'not_media': False,
                        'original_class': class_name
                    })
                    css_rules_parsed.append({
                        'selector': selector_base,
                        'rule_content': 'display: inline;',
                        'media_query': MEDIA_PREFIXES[pref['base']],
                        'pseudo_elements': [],
                        'important': False,
                        'not_media': False,
                        'original_class': class_name
                    })
                    continue

                if pref['base'].startswith("not:") and pref['base'][4:] in CANONICAL_MEDIA_NAMES and pref['not']:
                    base_media = pref['base'][4:]
                    css_rules_parsed.append({
                        'selector': selector_base,
                        'rule_content': 'display: none;',
                        'media_query': None,
                        'pseudo_elements': [],
                        'important': False,
                        'not_media': True,
                        'original_class': class_name
                    })
                    if base_media == "phone":
                        expr = "(min-width: 768px)"
                    elif base_media == "tablet":
                        expr = "(max-width: 767px), (min-width: 1025px)"
                    elif base_media == "mobile":
                        expr = "(min-width: 1025px)"
                    else:
                        expr = "(max-width: 1024px)"
                    css_rules_parsed.append({
                        'selector': selector_base,
                        'rule_content': 'display: inline;',
                        'media_query': expr,
                        'pseudo_elements': [],
                        'important': False,
                        'not_media': True,
                        'original_class': class_name
                    })
                    continue

                base_rule = style_for_base_class(pref['base'])
                if not base_rule:
                    continue

                selector = '.' + escape_class_selector(pref['original'])
                for pseudo in pref['pseudos']:
                    selector += f":{pseudo}"
                rule = base_rule.strip()
                if pref['important']:
                    rule = re.sub(r'(?<!important)\s*;', ' !important;', rule)
                mq = MEDIA_PREFIXES.get(pref['media'], None)
                css_rules_parsed.append({
                    'selector': selector,
                    'rule_content': rule,
                    'media_query': mq,
                    'pseudo_elements': pref['pseudos'],
                    'important': pref['important'],
                    'not_media': pref['not'],
                    'original_class': class_name
                })

        final_css_buckets = {}
        for info in css_rules_parsed:
            key = (info['media_query'], info['important'], tuple(info['pseudo_elements']), info['not_media'])
            final_css_buckets.setdefault(key, []).append(
                f"{info['selector']} {{\n    {info['rule_content']}\n}}"
            )

        sorted_keys = sorted(final_css_buckets.keys(), key=lambda k: (k[0] is not None, k[3], k[1]))
        new_css_rules_list = []
        for k in sorted_keys:
            rules = final_css_buckets[k]
            if k[0]:
                new_css_rules_list.append(f"@media {k[0]} {{\n" + "\n".join(rules) + "\n}}")
            else:
                new_css_rules_list.extend(rules)

        if css_rules_errors:
            new_css_rules_list.append("\n".join(css_rules_errors))

        new_css = "\n".join(new_css_rules_list)

        if new_css:
            head = soup.find('head')
            if head:
                style_tag = head.find('style')
                if style_tag:
                    style_tag.string = (style_tag.string or "") + "\n" + new_css
                else:
                    nt = soup.new_tag("style")
                    nt.string = new_css
                    head.append(nt)
                    nt.insert_after(NavigableString("\n"))
                return str(soup)
            else:
                nt = soup.new_tag("style")
                nt.string = new_css
                if soup.contents:
                    soup.insert(0, nt)
                    nt.insert_after(NavigableString("\n"))
                else:
                    soup.append(nt)
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

    def _add(self, comp: COMPONENT, __name__=None, __scripts__=None, __assets__=None, **kwargs):
        """
        Adds a component to the preview stack.
        Can optionally accept a __name__ for the component instance, and lists of __scripts__ and __assets__.
        """
        with self.lock:
            self.stack.append((comp, kwargs, __scripts__ or [], __assets__ or [], __name__))
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

    def __call__(self, comp=None, __scripts__=None, __assets__=None, **kwargs):
        if comp:
            with self.lock:
                self._clean()
                self._add(comp, __scripts=__scripts__, __assets=__assets__, **kwargs)
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
        from comp.mods.service import render
        html_parts = []
        for idx, (comp, kwargs, scripts, assets, _) in enumerate(self.stack):
            rendered = render(comp, __scripts__=scripts, __assets__=assets, **kwargs)
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
            _PREVIEW()._add(comp, __name__=__name__, __scripts__=__scripts__, __assets__=__assets__, **kwargs)
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
