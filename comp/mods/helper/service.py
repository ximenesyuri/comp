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
from typed import typed, Dict, Str, List
from comp.mods.helper.types import COMPONENT
from bs4 import BeautifulSoup, NavigableString
from comp.mods.err import StyleErr, MinifyErr, PreviewErr

@typed
def _style(html: Str) -> Str:
    try:
        soup = BeautifulSoup(html, "html.parser")
        for row in soup.find_all(class_="row"):
            cols = [
                c
                for c in row.find_all(recursive=False)
                if hasattr(c, "get")
                and c.get("class")
                and any(
                    re.fullmatch(r"col(?:-\d+)?", cl) for cl in c.get("class")
                )
            ]
            col_specs = []
            for col in cols:
                weight = None
                for cl in col.get("class", []):
                    m = re.fullmatch(r"col-(\d+)", cl)
                    if m:
                        weight = int(m.group(1))
                        break
                    elif cl == "col":
                        weight = 1
                if weight is not None:
                    col_specs.append((col, weight))
            total = sum(w for _, w in col_specs) or 1
            for col, w in col_specs:
                pct = w * 100.0 / total
                prev = col.get("style", "")
                rest = re.sub(r"(flex|width|max-width)\s*:[^;]+;", "", prev)
                col["style"] = (
                    rest
                    + f" flex: 0 0 {pct:.6f}%;"
                    + f" max-width: {pct:.6f}%;"
                ).strip()

        def escape_class_selector(cls: str) -> str:
            return (
                cls.replace(":", "\\:")
                .replace("#", "\\#")
                .replace("[", "\\[")
                .replace("]", "\\]")
                .replace(".", "\\.")
            )

        FONT_FAMILY_PATTERNS = [
            (re.compile(r"^(?:font-family-|ff-)(.+)$", re.I), ""),
            (re.compile(r"^(?:font-family-sans-|ff-sans-|ff-ss-|sans-)(.+)$", re.I), 'sans-serif'),
            (re.compile(r"^(?:font-family-serif-|ff-serif-|ff-s-|serif-)(.+)$", re.I), 'serif'),
            (re.compile(r"^(?:font-family-mono-|ff-mono-|ff-m-|mono-)(.+)$", re.I), 'monospace'),
        ]

        FONT_SIZE_KEYWORDS = {
            "font-size-xx-small": "xx-small", "xx-small": "xx-small", "fz-xx-small": "xx-small",
            "fz-xx-s": "xx-small", "fz-xxs": "xx-small",
            "font-size-x-small": "x-small", "x-small": "x-small", "fz-x-small": "x-small",
            "fz-x-s": "x-small", "fz-xs": "x-small",
            "font-size-small": "small", "small": "small", "fz-small": "small", "fz-s": "small",
            "font-size-medium": "medium", "medium": "medium", "fz-medium": "medium", "fz-m": "medium",
            "font-size-large": "large", "large": "large", "fz-large": "large", "fz-l": "large",
            "font-size-x-large": "x-large", "x-large": "x-large", "fz-x-large": "x-large", "fz-x-l": "x-large",
            "fz-xl": "x-large",
            "font-size-xx-large": "xx-large", "xx-large": "xx-large", "fz-xx-large": "xx-large",
            "fz-xx-l": "xx-large", "fz-xxl": "xx-large",
            "font-size-huge": "xxx-large", "huge": "xxx-large", "fz-huge": "xxx-large", "fz-h": "xxx-large",
            "fz-xxx-l": "xxx-large", "fz-xxxl": "xxx-large",
        }
        FONT_SIZE_VAL_PATTERN = re.compile(r"^(?:font-size-?|fz-)(\d+(?:\.\d+)?)(px|em|rem|%)$", re.I)

        FONT_WEIGHT_KEYWORDS = {
            "font-weight-xx-light": 100,
            "xx-light": 100, "fw-xx-l": 100, "fw-xxl": 100,
            "font-weight-x-light": 200,
            "x-light": 200, "fw-extra-light": 200, "fw-x-l": 200, "fw-xl": 200,
            "font-weight-light": 300, "light": 300, "fw-light": 300, "fw-l": 300,
            "font-weight-normal": 400, "normal": 400, "fw-normal": 400, "fw-n": 400,
            "font-weight-x-normal": 600,
            "x-normal": 600, "semi-bold": 600, "fw-x-normal": 600, "fw-semi-bold": 600,
            "fw-sb": 600, "fw-x-n": 600, "fw-xn": 600,
            "font-weight-bold": 700, "bold": 700, "fw-bold": 700, "fw-b": 700,
            "font-weight-x-bold": 800, "x-bold": 800, "fw-x-bold": 800,
            "fw-x-b": 800, "fw-xb": 800,
            "font-weight-xx-bold": 900, "Bold": 900, "xx-bold": 900, "fw-xx-bold": 900,
            "fw-black": 900, "fw-xxb": 900, "fw-B": 900,
        }
        FONT_WEIGHT_VAL_PATTERN = re.compile(r"^(?:font-weight-?|fw-)(\d{3})$", re.I)

        FONT_STYLE_ALIASES = {
            "font-style-italic": "italic", "italic": "italic", "it": "italic",
            "fs-italic": "italic", "fs-it": "italic", "fs-i": "italic",
        }
        COLOR_PATTERNS = (
            (re.compile(r"^(?:font-color-|color-|fc-)(.+)$", re.I),),
        )

        TEXT_ALIGN_ALIASES = {
            "text-align-center": ("text-align", "center"),
            "txt-alg-center": ("text-align", "center"),
            "txt-alg-cnt": ("text-align", "center"),
            "txt-alg-c": ("text-align", "center"),
            "ta-c": ("text-align", "center"),
            "text-align-left": ("text-align", "left"),
            "txt-alg-left": ("text-align", "left"),
            "txt-alg-lft": ("text-align", "left"),
            "txt-alg-l": ("text-align", "left"),
            "ta-l": ("text-align", "left"),
            "text-align-right": ("text-align", "right"),
            "txt-alg-right": ("text-align", "right"),
            "txt-alg-rgt": ("text-align", "right"),
            "txt-alg-r": ("text-align", "right"),
            "ta-r": ("text-align", "right"),
            "text-align-start": ("text-align", "start"),
            "txt-alg-start": ("text-align", "start"),
            "txt-alg-st": ("text-align", "start"),
            "txt-alg-s": ("text-align", "start"),
            "ta-s": ("text-align", "start"),
            "text-align-end": ("text-align", "end"),
            "txt-alg-end": ("text-align", "end"),
            "txt-alg-e": ("text-align", "end"),
            "ta-e": ("text-align", "end"),
            "text-align-justify": ("text-align", "justify"),
            "txt-alg-justify": ("text-align", "justify"),
            "txt-alg-just": ("text-align", "justify"),
            "txt-alg-jst": ("text-align", "justify"),
            "txt-alg-j": ("text-align", "justify"),
            "ta-j": ("text-align", "justify"),
        }
        TEXT_JUSTIFY_ALIASES = {
            "text-justify-none": ("text-justify", "none"),
            "txt-just-none": ("text-justify", "none"),
            "tj-none": ("text-justify", "none"),
            "tj-n": ("text-justify", "none"),
            "text-justify-auto": ("text-justify", "auto"),
            "txt-just-auto": ("text-justify", "auto"),
            "tj-auto": ("text-justify", "auto"),
            "tj-a": ("text-justify", "auto"),
            "text-justify-distribute": ("text-justify", "distribute"),
            "txt-just-distribute": ("text-justify", "distribute"),
            "tj-dist": ("text-justify", "distribute"),
            "tj-d": ("text-justify", "distribute"),
            "text-justify-word": ("text-justify", "inter-word"),
            "text-just-word": ("text-justify", "inter-word"),
            "tj-word": ("text-justify", "inter-word"),
            "tj-w": ("text-justify", "inter-word"),
            "text-justify-character": ("text-justify", "inter-character"),
            "text-just-char": ("text-justify", "inter-character"),
            "tj-char": ("text-justify", "inter-character"),
            "tj-c": ("text-justify", "inter-character"),
        }
        TEXT_WRAP_ALIASES = {
            "text-wrap": ("text-wrap", "wrap"),
            "wrap": ("text-wrap", "wrap"),
            "txt-wrap": ("text-wrap", "wrap"),
            "tw": ("text-wrap", "wrap"),
            "text-nowrap": ("text-wrap", "nowrap"),
            "nowrap": ("text-wrap", "nowrap"),
            "txt-nowrap": ("text-wrap", "nowrap"),
            "txt-wrap-none": ("text-wrap", "nowrap"),
            "tw-none": ("text-wrap", "nowrap"),
            "tw-no": ("text-wrap", "nowrap"),
            "tw-n": ("text-wrap", "nowrap"),
            "text-wrap-balance": ("text-wrap", "balance"),
            "txt-wrap-bal": ("text-wrap", "balance"),
            "tw-bal": ("text-wrap", "balance"),
            "tw-b": ("text-wrap", "balance"),
            "text-wrap-pretty": ("text-wrap", "pretty"),
            "txt-wrap-pretty": ("text-wrap", "pretty"),
            "txt-wrap-pty": ("text-wrap", "pretty"),
            "tw-pretty": ("text-wrap", "pretty"),
            "tw-pty": ("text-wrap", "pretty"),
            "tw-p": ("text-wrap", "pretty"),
        }
        TEXT_TRANSFORM_ALIASES = {
            "text-transform-uppercase": "uppercase",
            "uppercase": "uppercase",
            "upper": "uppercase",
            "txt-trans-upper": "uppercase",
            "tt-upper": "uppercase",
            "tt-u": "uppercase",
            "text-transform-lowercase": "lowercase",
            "lowercase": "lowercase",
            "lower": "lowercase",
            "txt-trans-lower": "lowercase",
            "tt-lower": "lowercase",
            "tt-l": "lowercase",
            "text-transform-capitalize": "capitalize",
            "capitalize": "capitalize",
            "cap": "capitalize",
            "txt-trans-cap": "capitalize",
            "tt-cap": "capitalize",
            "tt-c": "capitalize",
        }
        DECORATION_TYPE_MAP = {
            "underline": ["underline", "under", "txt-decor-under", "td-under", "td-u"],
            "overline": ["overline", "txt-decor-over", "td-over", "td-o"],
            "line-through": ["through", "txt-decor-thr", "td-thr", "td-t"],
        }
        DECORATION_TYPE_RE = "|".join(
            [
                "|".join([rf"{n}" for n in DECORATION_TYPE_MAP[variant]])
                for variant in DECORATION_TYPE_MAP
            ]
        )
        DECORATION_PATTERN = (
            rf"(?:text-decoration-)?(?P<variant>{DECORATION_TYPE_RE})-(?P<size>[\d\.]+)(?P<unit>px|em|rem|%)"
            rf"-(?P<color>#[\da-fA-F]+|rgb\(.*?\)|[a-zA-Z\-]+)"
            rf"-(?P<line>(solid|double|dotted|dashed|wavy|underline|overline|line-through))"
        )
        decopat = (
            rf"(?:{DECORATION_TYPE_RE})-(?P<size>[\d\.]+)(?P<unit>px|em|rem|%)"
            rf"-(?P<color>#[\da-fA-F]+|rgb\(.*?\)|[a-zA-Z\-]+)"
            rf"-(?P<line>(solid|double|dotted|dashed|wavy|underline|overline|line-through))"
        )

        def cls_lookup(d):
            return {k.lower(): v for k, v in d.items()}

        TEXT_ALIGN_ALIASES = cls_lookup(TEXT_ALIGN_ALIASES)
        TEXT_JUSTIFY_ALIASES = cls_lookup(TEXT_JUSTIFY_ALIASES)
        TEXT_WRAP_ALIASES = cls_lookup(TEXT_WRAP_ALIASES)
        TEXT_TRANSFORM_ALIASES = cls_lookup(TEXT_TRANSFORM_ALIASES)
        FONT_SIZE_KEYWORDS = cls_lookup(FONT_SIZE_KEYWORDS)
        FONT_WEIGHT_KEYWORDS = cls_lookup(FONT_WEIGHT_KEYWORDS)
        FONT_STYLE_ALIASES = cls_lookup(FONT_STYLE_ALIASES)

        DISPLAY_PROPERTY_MAP = {
            'display': 'display', 'd': 'display'
        }
        BOX_PROPERTY_MAP = {
            'margin': 'margin',   'm': 'margin',
            'margin-top':'margin-top','mt':'margin-top',
            'margin-right':'margin-right','mr':'margin-right',
            'margin-bottom':'margin-bottom','mb':'margin-bottom',
            'margin-left':'margin-left','ml':'margin-left',
            'padding':'padding',   'p':'padding',
            'padding-top':'padding-top','pt':'padding-top',
            'padding-right':'padding-right','pr':'padding-right',
            'padding-bottom':'padding-bottom','pb':'padding-bottom',
            'padding-left':'padding-left','pl':'padding-left',
            'gap':'gap', 'g':'gap'
        }
        SIZE_PROPERTY_MAP = {
            'width':'width','w':'width',
            'min-width':'min-width','mw':'min-width',
            'max-width':'max-width','xw':'max-width',
            'height':'height','h':'height',
            'min-height':'min-height','mh':'min-height',
            'max-height':'max-height','xh':'max-height'
        }
        BORDER_PROPERTY_MAP = {
            'border':'border','b':'border',
            'border-top':'border-top','bt':'border-top',
            'border-right':'border-right','br':'border-right',
            'border-bottom':'border-bottom','bb':'border-bottom',
            'border-left':'border-left','bl':'border-left',
            'border-radius':'border-radius','bR':'border-radius','radius':'border-radius'
        }
        BG_PROPERTY_MAP = {
            'background':'background',
            'background-color':'background-color','bg':'background-color',
            'background-size':'background-size','bgz':'background-size','bg-sz':'background-size',
            'background-image':'background-image','bgi':'background-image','bg-img':'background-image',
            'background-position':'background-position','bgp':'background-position','bg-pos':'background-position',
            'backdrop-filter':'backdrop-filter','drop':'backdrop-filter'
        }
        POSITION_PROPERTY_MAP = {
            'position':'position','pos':'position',
        }
        ZINDEX_PROPERTY_MAP = {
            'z-index':'z-index','z':'z-index'
        }
        OVERFLOW_PROPERTY_MAP = {
            'overflow':'overflow','ov':'overflow',
            'overflow-x':'overflow-x','ovx':'overflow-x',
            'overflow-y':'overflow-y','ovy':'overflow-y'
        }
        ALIGN_PROPERTY_MAP = {
            "align-items":"align-items", "align-it":"align-items", "alg-it":"align-items",
            "align":"text-align", "alg":"text-align",
            "justify-content":"justify-content", "just-cont":"justify-content",
            "justify-text":"text-align", "just-text":"text-align", "jst-txt":"text-align",
            "float":"float", "flt":"float"
        }
        PROPERTY_MAP = {}
        for m in (
            DISPLAY_PROPERTY_MAP,
            BOX_PROPERTY_MAP,
            SIZE_PROPERTY_MAP,
            BORDER_PROPERTY_MAP,
            BG_PROPERTY_MAP,
            POSITION_PROPERTY_MAP,
            ZINDEX_PROPERTY_MAP,
            OVERFLOW_PROPERTY_MAP,
            ALIGN_PROPERTY_MAP,
        ):
            PROPERTY_MAP.update(m)

        DISPLAY_VALUE_MAP = {
            'flex':'flex','flx':'flex',
            'inline':'inline','inl':'inline',
            'block':'block','blk':'block',
            'table':'table','tab':'table',
            'inline-block':'inline-block','inl-blk':'inline-block',
            'inline-flex':'inline-flex','inl-flx':'inline-flex'
        }

        MEDIA_PREFIXES = {
            "phone":  "(min-width: 0px) and (max-width: 767px)",
            "tablet": "(min-width: 768px) and (max-width: 1024px)",
            "mobile": "(min-width: 0px) and (max-width: 1024px)",
            "desktop":"(min-width: 1025px) and (max-width: 10000px)",
        }
        MEDIA_ALIASES = {
            "p": "phone",   "ph": "phone",
            "t": "tablet",  "tab": "tablet",
            "m": "mobile",  "mob": "mobile",
            "d": "desktop", "desk": "desktop", "dsk": "desktop",
        }

        PSEUDO_PREFIXES = {
            "hover":  "hover",  "h": "hover",
            "active": "active", "a": "active",
            "focus":  "focus",  "f": "focus",
        }
        PSEUDO_ORDER = ["hover", "active", "focus"]

        IMPORTANT_PREFIXES = {"!", "i", "important", "imp"}
        NOT_PREFIXES       = {"not", "n"}

        MEDIA_ALL   = set(MEDIA_PREFIXES) | set(MEDIA_ALIASES)
        PSEUDO_ALL  = set(PSEUDO_PREFIXES)
        IMP_ALL     = IMPORTANT_PREFIXES
        NOT_ALL     = NOT_PREFIXES

        def style_for_base_class(cls: str) -> str:
            lcls = cls.lower()

            for pat, base_family in FONT_FAMILY_PATTERNS:
                m = pat.fullmatch(cls)
                if m:
                    val = m.group(1)
                    ff = val.replace("_", " ").replace("-", " ")
                    family = f'"{ff}"'
                    if base_family:
                        family += f', {base_family}'
                    return f"font-family: {family};"

            if lcls in FONT_SIZE_KEYWORDS:
                sz = FONT_SIZE_KEYWORDS[lcls]
                return f"font-size: {sz};"
            m = FONT_SIZE_VAL_PATTERN.fullmatch(cls)
            if m:
                num, unit = m.group(1), m.group(2)
                return f"font-size: {num}{unit};"

            if lcls in FONT_WEIGHT_KEYWORDS:
                w = FONT_WEIGHT_KEYWORDS[lcls]
                return f"font-weight: {w};"
            m = FONT_WEIGHT_VAL_PATTERN.fullmatch(cls)
            if m:
                n = m.group(1)
                return f"font-weight: {n};"

            if lcls in FONT_STYLE_ALIASES:
                style = FONT_STYLE_ALIASES[lcls]
                return f"font-style: {style};"

            for color_pat in COLOR_PATTERNS:
                m = color_pat[0].fullmatch(cls)
                if m:
                    color = m.group(1)
                    if color.startswith("#") or color.startswith("rgb"):
                        return f"color: {color};"
                    var = color.replace("-", "_")
                    return f"color: var(--{var});"
            if lcls in TEXT_ALIGN_ALIASES:
                prop, val = TEXT_ALIGN_ALIASES[lcls]
                return f"{prop}: {val};"
            if lcls in TEXT_JUSTIFY_ALIASES:
                prop, val = TEXT_JUSTIFY_ALIASES[lcls]
                return f"{prop}: {val};"
            if lcls in TEXT_WRAP_ALIASES:
                prop, val = TEXT_WRAP_ALIASES[lcls]
                return f"{prop}: {val};"
            if lcls in TEXT_TRANSFORM_ALIASES:
                val = TEXT_TRANSFORM_ALIASES[lcls]
                return f"text-transform: {val};"

            m = re.fullmatch(DECORATION_PATTERN, cls)
            if m:
                variant = m.group("variant")
                size = m.group("size")
                unit = m.group("unit")
                color = m.group("color")
                line = m.group("line")
                for cssval, aliases in DECORATION_TYPE_MAP.items():
                    if variant in aliases:
                        variant = cssval
                        break
                value = (f"{variant} {size}{unit} {color} {line}")
                return f"text-decoration: {value};"

            m = re.fullmatch(decopat, cls)
            if m:
                variant = [
                    cssval
                    for cssval, als in DECORATION_TYPE_MAP.items()
                    if any(cls.startswith(a) for a in als)
                ]
                variant = variant[0] if variant else "underline"
                size, unit, color, line = (
                    m.group("size"),
                    m.group("unit"),
                    m.group("color"),
                    m.group("line"),
                )
                value = f"{variant} {size}{unit} {color} {line}"
                return f"text-decoration: {value};"

            display_shortcut = DISPLAY_VALUE_MAP.get(cls)
            if display_shortcut:
                return f"display: {display_shortcut};"

            if cls in (
                'flex-center', 'flx-cnt', 'flx-center', 'flex-cnt',
                'center', 'cnt', 'c'
            ):
                return "display: flex; justify-content: center; align-items: center;"

            aliases = {
                'left': r'(?:left|lft|l)',
                'right': r'(?:right|rgt|r)',
                'top': r'(?:top|t)',
                'bottom': r'(?:bottom|bot|btm|b)',
            }
            for horiz, vert, hpad, vpad in [
                ('left',   'top',    'padding-left',  'padding-top'),
                ('left',   'bottom', 'padding-left',  'padding-bottom'),
                ('right',  'top',    'padding-right', 'padding-top'),
                ('right',  'bottom', 'padding-right', 'padding-bottom')
            ]:
                pattern = rf"(?:flex-|flx-)?(?:{aliases[horiz]}-{aliases[vert]}|{horiz[0]}{vert[0]})-(.+?)-(.+)"
                m = re.fullmatch(pattern, cls)
                if m:
                    hval, vval = m.group(1), m.group(2)
                    justify = "flex-start" if horiz == "left" else "flex-end"
                    align   = "flex-start" if vert == "top"  else "flex-end"
                    return (
                        f"display: flex; align-items: {align}; justify-content: {justify}; "
                        f"{vpad}: {vval}; {hpad}: {hval};"
                    )
            top_aliases = aliases['top']
            bottom_aliases = aliases['bottom']
            left_aliases = aliases['left']
            right_aliases = aliases['right']

            m = re.fullmatch(
                rf"(?:flex-|flx-)?(?:{left_aliases}-{top_aliases}|lt)-(.+)", cls)
            if m:
                pad = m.group(1).strip()
                return (
                    "display: flex; align-items: flex-start; justify-content: flex-start;"
                    f" padding-top: {pad}; padding-left: {pad};"
                )
            m = re.fullmatch(
                rf"(?:flex-|flx-)?(?:{right_aliases}-{top_aliases}|rt)-(.+)", cls)
            if m:
                pad = m.group(1).strip()
                return (
                    "display: flex; align-items: flex-start; justify-content: flex-end;"
                    f" padding-top: {pad}; padding-right: {pad};"
                )
            m = re.fullmatch(
                rf"(?:flex-|flx-)?(?:{left_aliases}-{bottom_aliases}|lb)-(.+)", cls)
            if m:
                pad = m.group(1).strip()
                return (
                    "display: flex; align-items: flex-end; justify-content: flex-start;"
                    f" padding-bottom: {pad}; padding-left: {pad};"
                )
            m = re.fullmatch(
                rf"(?:flex-|flx-)?(?:{right_aliases}-{bottom_aliases}|rb)-(.+)", cls)
            if m:
                pad = m.group(1).strip()
                return (
                    "display: flex; align-items: flex-end; justify-content: flex-end;"
                    f" padding-bottom: {pad}; padding-right: {pad};"
                )
            m = re.fullmatch(rf"(?:flex-|flx-)?{top_aliases}-(.+)", cls)
            if m:
                pad = m.group(1).strip()
                return (
                    "display: flex; align-items: flex-start; justify-content: center;"
                    f" padding-top: {pad};"
                )
            m = re.fullmatch(rf"(?:flex-|flx-)?{bottom_aliases}-(.+)", cls)
            if m:
                pad = m.group(1).strip()
                return (
                    "display: flex; align-items: flex-end; justify-content: center;"
                    f" padding-bottom: {pad};"
                )

            m = re.fullmatch(rf"(?:flex-)?{left_aliases}-(.+)", cls)
            if m:
                pad_value = m.group(1).strip()
                return (
                    "display: flex; align-items: center; justify-content: flex-start;"
                    f" padding-left: {pad_value};"
                )
            m = re.fullmatch(rf"(?:flex-)?{right_aliases}-(.+)", cls)
            if m:
                pad_value = m.group(1).strip()
                return (
                    "display: flex; align-items: center; justify-content: flex-end;"
                    f" padding-right: {pad_value};"
                )

            m = re.fullmatch(r'(align-items|align-it|alg-it)-(.+)', cls)
            if m:
                val = FLEX_JUSTIFY_ALIGN_VALUE_MAP.get(m.group(2), m.group(2))
                return f"align-items: {val};"
            m = re.fullmatch(r'(align|alg)-(.+)', cls)
            if m:
                val = FLEX_JUSTIFY_ALIGN_VALUE_MAP.get(m.group(2), m.group(2))
                return f"text-align: {val};"
            m = re.fullmatch(r'(justify-content|just-cont)-(.+)', cls)
            if m:
                val = FLEX_JUSTIFY_ALIGN_VALUE_MAP.get(m.group(2), m.group(2))
                return f"justify-content: {val};"

            m = re.fullmatch(r'(?:position|pos)-(top|bottom|left|right|lft|btm|rgt|t|b|l|r)-(.+)', cls)
            if m:
                prop, value = m.groups()
                prop_map = {
                    't': 'top',
                    'lft': 'left', 'l': 'left',
                    'btm': 'bottom', 'b': 'bottom',
                    'rgt': 'right', 'r': 'right'
                }
                prop = prop_map.get(prop, prop)
                return f"{prop}: {value.strip()};"

            if cls == "row":
                return "display: flex; flex-wrap: wrap;"
            if cls == "col":
                return "flex: 1 0 0%;"
            m = re.fullmatch(r"col-(\d+)", cls)
            if m:
                n = int(m.group(1))
                total = 5
                if 1 <= n <= total:
                    pct = n * 100.0 / total
                    return (f"flex: 0 0 {pct:.6f}%;"
                            f" max-width: {pct:.6f}%;")
            m2 = re.fullmatch(r"([-a-z0-9]+)-(.+)", cls, re.I)
            if m2:
                alias, raw = m2.groups()
                prop = PROPERTY_MAP.get(alias)
                if prop:
                    val = raw

                    if re.fullmatch(r"\d+(\.\d+)?", val):
                        val += "px"

                    if prop == "font-weight":
                        val = str(FONT_WEIGHT_MAP.get(val, val))
                    elif prop == "font-style":
                        val = FONT_STYLE_MAP.get(val, val)
                    elif prop == "text-decoration":
                        val = TEXT_DECORATION_MAP.get(val, val)
                    elif prop == "text-transform":
                        val = TEXT_TRANSFORM_MAP.get(val, val)
                    elif prop == "text-align":
                        val = TEXT_ALIGN_VALUE_MAP.get(val, val)
                    elif prop == "display":
                        val = DISPLAY_VALUE_MAP.get(val, val)
                    elif prop == "position":
                        val = POSITION_VALUE_MAP.get(val, val)
                    elif prop in ("color", "background-color", "fill") and not (
                            val.startswith("#") or val.startswith("rgb") or val.startswith("var(")):
                        var = val.replace("-", "_")
                        val = f"var(--{var})"
                    elif prop == "backdrop-filter":
                        val = f"blur({val})"

                    return f"{prop}: {val};"

            return None

        def parse_prefixed_class(class_name: str):
            parts = class_name.split(':')
            orig = class_name
            found_media = None
            found_pseudos = []
            found_important = False
            found_not = False
            i = 0
            while i < len(parts):
                p = parts[i].lower()
                if p in NOT_ALL:
                    if i != 0 or i+1 >= len(parts) or parts[i+1].lower() not in MEDIA_ALL:
                        return {'error': f"ERROR({orig})"}
                    found_not = True
                    i += 1
                elif p in IMP_ALL:
                    found_important = True
                    i += 1
                elif p in MEDIA_ALL:
                    if found_media is not None:
                        return {'error': f"ERROR({orig})"}
                    found_media = MEDIA_ALIASES.get(p, p)
                    i += 1
                elif p in PSEUDO_ALL:
                    pseudo = PSEUDO_PREFIXES[p]
                    if pseudo in found_pseudos:
                        return {'error': f"ERROR({orig})"}
                    found_pseudos.append(pseudo)
                    i += 1
                else:
                    break
            base = ":".join(parts[i:])
            if not base:
                if found_media:
                    base = orig
                else:
                    return {'error': f"ERROR({orig})"}
            found_pseudos.sort(key=lambda x: PSEUDO_ORDER.index(x))
            return {
                'error': None,
                'important': found_important,
                'media': found_media,
                'pseudos': found_pseudos,
                'not': found_not,
                'base': base,
                'original': orig
            }

        CANONICAL_MEDIA = ["phone","tablet","mobile","desktop"]
        css_parsed = []
        css_errors = []

        for tag in soup.find_all(True):
            if not tag.has_attr('class'):
                continue
            for cls in tag['class']:
                pref = parse_prefixed_class(cls)
                if pref['error']:
                    css_errors.append(
                        f".{escape_class_selector(cls)} {{"
                        f" color: red; font-weight: bold;"
                        f" content: '{pref['error']}'; }}"
                    )
                    continue

                if pref['base'] in CANONICAL_MEDIA and not pref['not']:
                    sel = '.' + escape_class_selector(pref['original'])
                    css_parsed.append({
                        'selector': sel,
                        'rule_content': 'display: none;',
                        'media_query': None,
                        'pseudos': [],
                        'important': False,
                        'not_media': False
                    })
                    css_parsed.append({
                        'selector': sel,
                        'rule_content': 'display: inline;',
                        'media_query': MEDIA_PREFIXES[pref['base']],
                        'pseudos': [],
                        'important': False,
                        'not_media': False
                    })
                    continue

                if pref['not'] and pref['base'] in CANONICAL_MEDIA:
                    base = pref['base']
                    sel = '.' + escape_class_selector(pref['original'])
                    css_parsed.append({
                        'selector': sel,
                        'rule_content': 'display: none;',
                        'media_query': None,
                        'pseudos': [],
                        'important': False,
                        'not_media': True
                    })
                    if base == "phone":
                        expr = "(min-width: 768px)"
                    elif base == "tablet":
                        expr = "(max-width: 767px), (min-width: 1025px)"
                    elif base == "mobile":
                        expr = "(min-width: 1025px)"
                    else:
                        expr = "(max-width: 1024px)"
                    css_parsed.append({
                        'selector': sel,
                        'rule_content': 'display: inline;',
                        'media_query': expr,
                        'pseudos': [],
                        'important': False,
                        'not_media': True
                    })
                    continue

                base_rule = style_for_base_class(pref['base'])
                if not base_rule:
                    continue

                selector = '.' + escape_class_selector(pref['original'])
                for ps in pref['pseudos']:
                    selector += f":{ps}"

                rule = base_rule.strip()
                if pref['important']:
                    rule = re.sub(r';\s*$', ' !important;', rule)

                css_parsed.append({
                    'selector': selector,
                    'rule_content': rule,
                    'media_query': MEDIA_PREFIXES.get(pref['media']),
                    'pseudos': pref['pseudos'],
                    'important': pref['important'],
                    'not_media': pref['not']
                })

        buckets = {}
        for info in css_parsed:
            key = (info['media_query'],
                   info['important'],
                   tuple(info['pseudos']),
                   info['not_media'])
            rule = f"{info['selector']} {{\n    {info['rule_content']}\n}}"
            buckets.setdefault(key, []).append(rule)

        keys = sorted(buckets,
                      key=lambda k: (k[0] is not None, k[3], k[1]))
        final_rules = []
        for k in keys:
            seen = set()
            rules = []
            for r in buckets[k]:
                if r not in seen:
                    seen.add(r)
                    rules.append(r)
            if k[0]:
                final_rules.append(f"@media {k[0]} {{\n" + "\n".join(rules) + "\n}}")
            else:
                final_rules.extend(rules)

        if css_errors:
            final_rules.append("\n".join(css_errors))

        new_css = "\n".join(final_rules)

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

@typed
def _minify(html: Str) -> Str:
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
    html = re.sub(r'>\s{2,}<', '> <', html)
    html = re.sub(r'\s{2,}', ' ', html)
    html = re.sub(r'[\n\t\r]', '', html)
    html = re.sub(r'>\s+', '> ', html)
    html = re.sub(r'\s+<', ' <', html)
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
                print("[preview] Watching", src, "mtime", self.source_cache[src])
            except FileNotFoundError:
                pass
        else:
            print("[preview] Could not resolve file for object:", obj)

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
