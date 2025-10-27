from typed import typed, Str, Any, Maybe
from comp.mods.err import HelperErr
from comp.models import (
    Div,
    Alpine,
    Text,
    Title,
    Button,
    Link,
    Image,
    Globals,
    Script,
    Figure,
    Asset,
    Item,
    Unordered,
    Ordered,
    Nav,
    Header,
    Footer,
    Aside,
    Sidebar,
    Icon,
    Input,
    Column,
    Row,
    Grid,
    Head,
    Main,
    Body,
    Page,
    Metadata,
    Logo,
    Search
)

@typed
def if_key(entry: Any=None, what: Str="") -> Str:
    try:
        if entry is not None and entry != "":
            return f' {what}="{entry}"'
        return ""
    except Exception as e:
        raise HelperErr(e)

@typed
def if_bool(entry: Any=None, what: Str="") -> Str:
    try:
        if entry:
            return f" {what}"
        return ""
    except Exception as e:
        raise HelperErr(e)

@typed
def if_size(size: Any=None, key_w: Str="width", key_h: Str="height") -> Str:
    try:
        if size is not None and size != "":
            return f' {key_w}="{size}" {key_h}="{size}"'
        return ""
    except Exception as e:
        raise HelperErr(e)

@typed
def if_defined(entry: Any=None, default: Any="") -> Str:
    try:
        if entry:
            return entry
        return default
    except Exception as e:
        raise HelperErr(e)

@typed
def if_aria(aria: Any=None) -> Str:
    try:
        if not aria:
            return ""
        result = ""
        for field, name in [
            ("aria_label",       "aria-label"),
            ("aria_labelledby",  "aria-labelledby"),
            ("aria_describedby", "aria-describedby"),
            ("aria_controls",    "aria-controls"),
            ("aria_current",     "aria-current"),
            ("aria_details",     "aria-details"),
            ("aria_live",        "aria-live"),
            ("aria_pressed",     "aria-pressed"),
            ("aria_checked",     "aria-checked"),
            ("aria_valuemax",    "aria-valuemax"),
            ("aria_valuemin",    "aria-valuemin"),
            ("aria_valuenow",    "aria-valuenow"),
            ("aria_valuetext",   "aria-valuetext"),
        ]:
            val = getattr(aria, field, None)
            if val is not None:
                result += if_key(val, name)
        for field, name in [
            ("aria_disabled", "aria-disabled"),
            ("aria_expanded", "aria-expanded"),
            ("aria_hidden",   "aria-hidden"),
            ("aria_readonly","aria-readonly"),
            ("aria_selected","aria-selected"),
            ("aria_required","aria-required"),
        ]:
            if getattr(aria, field, False):
                result += if_bool(True, name)
        if getattr(aria, "aria_role", None):
            result += if_key(aria.aria_role, "role")
        extra = getattr(aria, "aria_attrs", None)
        if extra:
            for key, val in extra.items():
                if key and val is not None:
                    result += f' {key}="{val}"'
        return result
    except Exception as e:
        raise HelperErr(e)

@typed
def if_globals(globals: Maybe(Globals) = None) -> Str:
    try:
        if not globals:
            return ""
        return (
            if_key(globals.title,     "title")
          + if_key(globals.tabindex, "tabindex")
          + if_key(globals.accesskey,"accesskey")
          + if_key(globals.anchor,   "anchor")
          + if_bool(globals.hidden,  "hidden")
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_id(entry: Any = None) -> Str:
    try:
        return if_key(entry, "id")
    except Exception as e:
        raise HelperErr(e)

@typed
def if_class(entry: Any = None) -> Str:
    try:
        return if_key(entry, "class")
    except Exception as e:
        raise HelperErr(e)

@typed
def if_style(entry: Any = None) -> Str:
    try:
        return if_key(entry, "style")
    except Exception as e:
        raise HelperErr(e)

@typed
def if_div(div: Maybe(Div)=Div()) -> Str:
    try:
        if not div:
            return ""
        return (
            if_globals(div.div_globals)
          + if_aria(div.div_aria)
          + if_id(div.div_id)
          + if_class(div.div_class)
          + if_style(div.div_style)
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_alpine(alpine: Maybe(Alpine)=Alpine()) -> Str:
    try:
        if not alpine:
            return ""
        return (
            if_key(alpine.x_init, "x-init")
          + if_key(alpine.x_if,   "x-if")
          + if_key(alpine.x_show, "x-show")
          + if_key(alpine.x_data, "x-data")
          + if_bool(alpine.x_cloak, "x-cloak")
        )

    except Exception as e:
        raise HelperErr(e)

@typed
def if_header(header: Maybe(Header)=Header()) -> Str:
    try:
        if not header:
            return ""
        return (
            if_globals(header.header_globals)
          + if_aria(header.header_aria)
          + if_id(header.header_id)
          + if_class(header.header_class)
          + if_style(header.header_style)
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_aside(aside: Maybe(Aside)=Aside()) -> Str:
    try:
        if not aside:
            return ""
        return (
            if_globals(aside.aside_globals)
          + if_aria(aside.aside_aria)
          + if_id(aside.aside_id)
          + if_class(aside.aside_class)
          + if_style(aside.aside_style)
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_sidebar(sidebar: Maybe(Sidebar)=Sidebar()) -> Str:
    try:
        if not sidebar:
            return ""
        return (
            if_globals(sidebar.sidebar_globals)
          + if_aria(sidebar.sidebar_aria)
          + if_id(sidebar.sidebar_id)
          + if_class(sidebar.sidebar_class)
          + if_style(sidebar.sidebar_style)
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_footer(footer: Maybe(Footer)=Footer()) -> Str:
    try:
        if not footer:
            return ""
        return (
            if_globals(footer.footer_globals)
          + if_aria(footer.footer_aria)
          + if_key(footer.footer_id, "id")
          + if_key(footer.footer_class, "class")
          + if_key(footer.footer_style, "style")
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_head(head: Maybe(Head)=Head()) -> Str:
    try:
        if not head:
            return ""
        return (
            if_globals(head.head_globals)
          + if_aria(head.head_aria)
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_main(main: Maybe(Main)=Main()) -> Str:
    try:
        if not main:
            return ""
        return (
            if_globals(main.main_globals)
          + if_aria(main.main_aria)
          + if_key(main.main_id, "id")
          + if_key(main.main_class, "class")
          + if_key(main.main_style, "style")
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_body(body: Maybe(Body)=Body()) -> Str:
    try:
        if not body:
            return ""
        return (
            if_globals(body.body_globals)
          + if_aria(body.body_aria)
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_page(page: Maybe(Page)=Page()) -> Str:
    try:
        return ""
    except Exception as e:
        raise HelperErr(e)

@typed
def if_col(col: Maybe(Column)=Column()) -> Str:
    try:
        if not col:
            return ""
        return (
            if_globals(col.col_globals)
          + if_aria(col.col_aria)
          + if_key(col.col_id,    "id")
          + if_key(col.col_class, "class")
          + if_key(col.col_style, "style")
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_row(row: Maybe(Row)=Row()) -> Str:
    try:
        if not row:
            return ""
        return (
            if_globals(row.row_globals)
          + if_aria(row.row_aria)
          + if_key(row.row_id,    "id")
          + if_key(row.row_class, "class")
          + if_key(row.row_style, "style")
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_grid(grid: Maybe(Grid)=Grid()) -> Str:
    try:
        if not grid:
            return ""
        return (
            if_globals(grid.grid_globals)
          + if_aria(grid.grid_aria)
          + if_key(grid.grid_id,    "id")
          + if_key(grid.grid_class, "class")
          + if_key(grid.grid_style, "style")
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_text(text: Maybe(Text)=Text()) -> Str:
    try:
        if not text:
            return ""
        return (
            if_globals(text.text_globals)
          + if_aria(text.text_aria)
          + if_id(text.text_id)
          + if_class(text.text_class)
          + if_style(text.text_style)
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_title(title: Maybe(Title)=Title()) -> Str:
    try:
        if not title:
            return ""
        return (
            if_globals(title.title_globals)
          + if_aria(title.title_aria)
          + if_id(title.title_id)
          + if_class(title.title_class)
          + if_style(title.title_style)
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_link(link: Maybe(Link)=Link()) -> Str:
    try:
        if not link:
            return ""
        return (
            if_globals(link.link_globals)
          + if_aria(link.link_aria)
          + if_id(link.link_id)
          + if_class(link.link_class)
          + if_style(link.link_style)
          + if_key(link.link_href,     "href")
          + if_key(link.link_download, "download")
          + if_key(link.link_rel,      "rel")
          + if_key(link.link_target,   "target")
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_button(button: Maybe(Button)=Button()) -> Str:
    try:
        if not button:
            return ""
        return (
            if_globals(button.button_globals)
          + if_aria(button.button_aria)
          + if_id(button.button_id)
          + if_class(button.button_class)
          + if_style(button.button_style)
          + if_key(button.on_click,   "@on_click")
          + if_key(button.click_away, "@click_away")
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_img(img: Maybe(Image)=Image()) -> Str:
    try:
        if not img:
            return ""
        return (
            if_globals(img.img_globals)
          + if_aria(img.img_aria)
          + if_id(img.img_id)
          + if_class(img.img_class)
          + if_style(img.img_style)
          + if_key(img.img_lazy, "loading")
          + if_key(img.img_alt,  "alt")
          + if_key(img.img_src,  "src")
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_figure(figure: Maybe(Figure)=Figure()) -> Str:
    try:
        if not figure:
            return ""
        return (
            if_globals(figure.figure_globals)
          + if_aria(figure.figure_aria)
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_script(script: Maybe(Script)=Script()) -> Str:
    try:
        if not script:
            return ""
        return (
            if_globals(script.script_globals)
          + if_aria(script.script_aria)
          + if_key(script.script_src,  "src")
          + if_key(script.script_type, "type")
          + if_bool(script.script_defer, "defer")
          + if_bool(script.script_async, "async")
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_asset(asset: Maybe(Asset)=Asset()) -> Str:
    try:
        if not asset:
            return ""
        return (
            if_globals(asset.asset_globals)
          + if_aria(asset.asset_aria)
          + if_key(asset.asset_href, "href")
          + if_key(asset.asset_mime, "type")
          + if_key(asset.asset_rel,  "rel")
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_item(item: Maybe(Item)=Item()) -> Str:
    try:
        if not item:
            return ""
        return (
            if_globals(item.item_globals)
          + if_aria(item.item_aria)
          + if_id(item.item_id)
          + if_class(item.item_class)
          + if_style(item.item_style)
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_ul(ul: Maybe(Unordered)=Unordered()) -> Str:
    try:
        if not ul:
            return ""
        return (
            if_globals(ul.ul_globals)
          + if_aria(ul.ul_aria)
          + if_id(ul.ul_id)
          + if_class(ul.ul_class)
          + if_style(ul.ul_style)
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_ol(ol: Maybe(Ordered)=Ordered()) -> Str:
    try:
        if not ol:
            return ""
        return (
            if_globals(ol.ol_globals)
          + if_aria(ol.ol_aria)
          + if_id(ol.ol_id)
          + if_class(ol.ol_class)
          + if_style(ol.ol_style)
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_nav(nav: Maybe(Nav)=Nav()) -> Str:
    try:
        if not nav:
            return ""
        return (
            if_globals(nav.nav_globals)
          + if_aria(nav.nav_aria)
          + if_id(nav.nav_id)
          + if_class(nav.nav_class)
          + if_style(nav.nav_style)
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_icon(icon: Maybe(Icon)=Icon()) -> Str:
    try:
        if not icon:
            return ""
        return (
            if_globals(icon.icon_globals)
          + if_alpine(icon.icon_aria)
          + if_id(icon.icon_id)
          + if_class(icon.icon_class)
          + if_style(icon.icon_style)
          + if_key(icon.icon_viewbox, "viewBox")
          + if_size(icon.icon_size)
          + if_key(icon.icon_fill,   "fill")
          + if_key(icon.icon_stroke, "stroke")
          + if_key(getattr(icon, "icon_stroke_width", None), "stroke-width")
        )
    except Exception as e:
        raise HelperErr(e)

@typed
def if_input(input: Maybe(Input)=Input()) -> Str:
    try:
        if not input:
            return ""
        return (
            if_globals(input.input_globals)
          + if_aria(input.input_aria)
          + if_id(input.input_id)
          + if_class(input.input_class)
          + if_style(input.input_style)
          + if_key(input.input_type,        "type")
          + if_key(input.input_placeholder, "placeholder")
          + if_key(input.input_value,       "value")
          + if_key(input.input_name,        "name")
          + if_key(input.input_autocomplete,"autocomplete")
          + if_bool(input.input_required,   "required")
          + if_bool(input.input_disabled,   "disabled")
          + if_bool(input.input_readonly,   "readonly")
          + if_bool(input.input_autofocus,  "autofocus")
          + if_key(input.input_tabindex,    "tabindex")
          + if_key(input.input_form_id,     "form")
          + if_key(input.input_minlength,   "minlength")
          + if_key(input.input_maxlength,   "maxlength")
          + if_key(input.input_pattern,     "pattern")
          + if_key(input.input_size,        "size")
          + if_key(input.input_min,         "min")
          + if_key(input.input_max,         "max")
          + if_key(input.input_step,        "step")
          + if_bool(input.input_multiple,   "multiple")
          + if_key(getattr(input, "input_accept", None), "accept")
          + if_bool(input.input_checked,    "checked")
          + if_key(getattr(input, "input_for", None),    "for")
        )
    except Exception as e:
        raise HelperErr(e)

def _render_inner(obj):
    try:
        if obj is None:
            return ""
        from comp.comps.content    import text, title, link, img, figure, button, logo
        from comp.comps.lists      import item, unordered, ordered, nav
        from comp.comps.includes   import asset, script
        from comp.comps.buttons    import button_close, button_menu, button_search, button_home, button_theme_switcher
        from comp.comps.extensions import alpine, search, search_script
        from comp.comps.form       import input
        from comp.comps.responsive import desktop, tablet, phone, mobile, not_desktop, not_tablet, not_phone, not_mobile
        from comp.comps.structure  import (
            div, header, footer, aside, body, head, page,
            col, col_1, col_2, col_3, col_4, col_5, row, grid
        )

        if isinstance(obj, Text):       return text(obj)
        if isinstance(obj, Title):      return title(obj)
        if isinstance(obj, Link):       return link(obj)
        if isinstance(obj, Image):      return img(obj)
        if isinstance(obj, Figure):     return figure(obj)
        if isinstance(obj, Button):     return button(obj)
        if isinstance(obj, Logo):       return logo(obj)
        if isinstance(obj, Item):       return item(obj)
        if isinstance(obj, Unordered):  return unordered(obj)
        if isinstance(obj, Ordered):    return ordered(obj)
        if isinstance(obj, Nav):        return nav(obj)
        if isinstance(obj, Script):     return script(obj)
        if isinstance(obj, Asset):      return asset(obj)
        if isinstance(obj, Alpine):     return alpine(obj)
        if isinstance(obj, Search):     return search(obj)
        if isinstance(obj, Input):      return input(obj)
        if isinstance(obj, Div):        return div(obj)
        if isinstance(obj, Header):     return header(obj)
        if isinstance(obj, Footer):     return footer(obj)
        if isinstance(obj, Main):       return main(obj)
        if isinstance(obj, Body):       return body(obj)
        if isinstance(obj, Head):       return head(obj)
        if isinstance(obj, Page):       return page(obj)
        if isinstance(obj, Aside):      return aside(obj)
        if isinstance(obj, Column):     return col(obj)
        if isinstance(obj, Row):        return row(obj)
        if isinstance(obj, Grid):       return grid(obj)
        if isinstance(obj, str):        return obj
        return str(obj)
    except Exception as e:
        raise HelperErr(e)

@typed
def _generate_meta_tags(meta: Maybe(Metadata)=Metadata()) -> Str:
    try:
        tags = []
        # Essential
        if meta.meta_charset:
            tags.append(f'<meta charset="{meta.meta_charset}"/>')
        if meta.meta_viewport:
            tags.append(f'<meta name="viewport" content="{meta.meta_viewport}"/>')
        if meta.meta_title:
            tags.append(f'<title>{meta.meta_title}</title>')
        # Standard SEO
        if meta.meta_description:
            tags.append(f'<meta name="description" content="{meta.meta_description}"/>')
        if meta.meta_keywords:
            tags.append(f'<meta name="keywords" content="{", ".join(meta.meta_keywords)}"/>')
        if meta.meta_author:
            tags.append(f'<meta name="author" content="{meta.meta_author}"/>')
        if meta.meta_publisher:
            tags.append(f'<meta name="publisher" content="{meta.meta_publisher}"/>')
        if meta.meta_copyright:
            tags.append(f'<meta name="copyright" content="{meta.meta_copyright}"/>')
        if meta.meta_robots:
            tags.append(f'<meta name="robots" content="{", ".join(meta.meta_robots)}"/>')
        if meta.meta_generator:
            tags.append(f'<meta name="generator" content="{meta.meta_generator}"/>')
        # Open Graph
        if meta.og_title:
            tags.append(f'<meta property="og:title" content="{meta.og_title}"/>')
        if meta.og_description:
            tags.append(f'<meta property="og:description" content="{meta.og_description}"/>')
        if meta.og_type:
            tags.append(f'<meta property="og:type" content="{meta.og_type}"/>')
        if meta.og_url:
            tags.append(f'<meta property="og:url" content="{meta.og_url}"/>')
        if meta.og_image:
            tags.append(f'<meta property="og:image" content="{meta.og_image}"/>')
        if meta.og_image_alt:
            tags.append(f'<meta property="og:image:alt" content="{meta.og_image_alt}"/>')
        if meta.og_locale:
            tags.append(f'<meta property="og:locale" content="{meta.og_locale}"/>')
        if meta.og_site_name:
            tags.append(f'<meta property="og:site_name" content="{meta.og_site_name}"/>')
        # Twitter Cards
        if meta.twitter_card:
            tags.append(f'<meta name="twitter:card" content="{meta.twitter_card}"/>')
        if meta.twitter_site:
            tags.append(f'<meta name="twitter:site" content="{meta.twitter_site}"/>')
        if meta.twitter_creator:
            tags.append(f'<meta name="twitter:creator" content="{meta.twitter_creator}"/>')
        if meta.twitter_title:
            tags.append(f'<meta name="twitter:title" content="{meta.twitter_title}"/>')
        if meta.twitter_description:
            tags.append(f'<meta name="twitter:description" content="{meta.twitter_description}"/>')
        if meta.twitter_image:
            tags.append(f'<meta name="twitter:image" content="{meta.twitter_image}"/>')
        if meta.twitter_image_alt:
            tags.append(f'<meta name="twitter:image:alt" content="{meta.twitter_image_alt}"/>')
        # Apple Specific
        if meta.apple_pwa_capable is True:
            tags.append(f'<meta name="apple-mobile-web-app-capable" content="true"/>')
        if meta.apple_pwa_status_bar_style:
            tags.append(f'<meta name="apple-mobile-web-app-status-bar-style" content="{meta.apple_pwa_status_bar_style}"/>')
        if meta.apple_pwa_title:
            tags.append(f'<meta name="apple-mobile-web-app-title" content="{meta.apple_pwa_title}"/>')
        # Microsoft/Windows Specific
        if meta.ms_tile_color:
            tags.append(f'<meta name="msapplication-TileColor" content="{meta.ms_tile_color}"/>')
        if meta.ms_tile_image:
            tags.append(f'<meta name="msapplication-TileImage" content="{meta.ms_tile_image}"/>')
        # Link-based Metadata (using <link> tags or special meta for theme-color)
        if meta.canonical:
            tags.append(f'<link rel="canonical" href="{meta.canonical}"/>')
        if meta.favicon:
            tags.append(f'<link rel="icon" href="{meta.favicon}"/>')
        if meta.apple_touch_icon:
            tags.append(f'<link rel="apple-touch-icon" href="{meta.apple_touch_icon}"/>')
        if meta.apple_mask_icon and meta.apple_mask_icon_color:
            tags.append(f'<link rel="mask-icon" href="{meta.apple_mask_icon}" color="{meta.mask_icon_color}"/>')
        if meta.theme_color:
            tags.append(f'<meta name="theme-color" content="{meta.theme_color}"/>')
        if meta.manifest:
            tags.append(f'<link rel="manifest" href="{meta.manifest}"/>')
        if meta.alternate_hreflang:
            for lang, url in meta.alternate_hreflang.items():
                tags.append(f'<link rel="alternate" hreflang="{lang}" href="{url}"/>')
        if meta.prefetch:
            for url in meta.prefetch:
                tags.append(f'<link rel="prefetch" href="{url}"/>')
        if meta.preload:
            for url in meta.preload:
                tags.append(f'<link rel="preload" href="{url}"/>')
        if meta.dns_prefetch:
            for url in meta.dns_prefetch:
                tags.append(f'<link rel="dns-prefetch" href="{url}"/>')
        if meta.preconnect:
            for url in meta.preconnect:
                tags.append(f'<link rel="preconnect" href="{url}"/>')
        # Custom Meta Tags
        if meta.custom_meta:
            for name, content in meta.custom_meta.items():
                tags.append(f'<meta name="{name}" content="{content}"/>')

        return "\n    ".join(tags)
    except Exception as e:
        raise HelperErr(e)
