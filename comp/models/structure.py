from typed import Str, Any, Enum, List, Dict, Url, PathUrl, Bool, HEX, Extension
from typed.models import optional
from comp.models.base import Globals, Aria
from comp.models.includes import Script, Asset

@optional
class Div:
    div_globals: Globals=Globals()
    div_aria:    Aria=Aria()
    div_id:      Str
    div_class:   Str
    div_style:   Str
    div_inner:   Any

Div.__display__ = "Div"

@optional
class Flex(Div):
    div_class:     Str='display: flex'
    div_direction: Enum(Str, 'row', 'column')

Flex.__display__ = "Flex"

@optional
class Inline(Div):
    div_class: Str="display: inline"

Inline.__display__ = "Inline"

@optional
class Block(Div):
    div_class: Str="display: block"

Block.__display__ = "Block"

@optional
class Metadata:
    meta_charset:     Str = "utf-8"
    meta_viewport:    Str = "width=device-width, initial-scale=1"
    meta_title:       Str
    meta_description: Str
    meta_keywords:    List(Str)
    meta_author:      Str
    meta_publisher:   Str
    meta_copyright:   Str
    meta_robots:      List(Enum(Str, 'index', 'follow', 'noindex', 'nofollow', 'noarchive', 'nosnippet', 'max-snippet:50'))=['index', 'follow']
    meta_generator:   Str
    canonical:        Url('http', 'https')
    favicon:          Extension('png', 'jpg', 'jpeg', 'webp')='/assets/favicon.png'
    theme_color:      HEX
    manifest:         Extension('json')='/assets/manifest.json'
    alternate_hreflang: Dict(Url('http', 'https'))
    prefetch:         List(PathUrl)
    preload:          List(PathUrl)
    dns_prefetch:     List(PathUrl)
    preconnect:       List(PathUrl)
    og_title:         Str
    og_description:   Str
    og_type:          Enum(Str, 'website', 'article', 'video.movie', 'music.song', 'profile', 'book')='website'
    og_url:           Url('http', 'https')
    og_image:         PathUrl
    og_image_alt:     Str
    og_locale:        Str
    og_site_name:     Str
    twitter_card:        Enum(Str, 'summary', 'summary_large_image', 'app', 'player')='summary'
    twitter_site:        Str
    twitter_creator:     Str
    twitter_title:       Str
    twitter_description: Str
    twitter_image:       PathUrl
    twitter_image_alt:   Str
    apple_pwa_capable:          Bool
    apple_pwa_status_bar_style: Enum(Str, 'default', 'black', 'black-translucent')='default'
    apple_pwa_title:            Str
    apple_touch_icon:           Extension('png', 'jpg', 'jpeg', 'webp')='/assets/apple-touch-icon.png'
    apple_mask_icon:            Extension('svg')='assets/apple-mask-icon.svg'
    apple_mark_icon_color:      HEX
    ms_tile_color: HEX='#0072C6'
    ms_tile_image: Extension('png', 'jpg', 'jpeg', 'webp')='/assets/ms-icon.png'
    custom_meta: Dict(Str)

Metadata.__display__ = "Metadata"

@optional
class Head:
    head_globals: Globals=Globals()
    head_aria:    Aria=Aria()
    head_meta:    Metadata=Metadata()
    head_assets:  List(Asset)=[]
    head_scripts: List(Script)=[]
    head_inner:   Any

Head.__display__ = "Head"

@optional
class Header:
    header_globals: Globals=Globals()
    header_aria:    Aria=Aria()
    header_id:      Str="header"
    header_class:   Str
    header_style:   Str
    header_inner:   Any

Header.__display__ = "Header"

@optional
class Footer:
    footer_globals: Globals=Globals()
    footer_aria:    Aria=Aria()
    footer_id:      Str="footer"
    footer_class:   Str
    footer_style:   Str
    footer_inner:   Any

Footer.__display__ = "Footer"

@optional
class Aside:
    aside_globals: Globals=Globals()
    aside_aria:    Aria=Aria()
    aside_id:      Str="aside"
    aside_class:   Str
    aside_style:   Str
    aside_inner:   Any

Aside.__display__ = "Aside"

@optional
class Sidebar:
    sidebar_globals: Globals=Globals()
    sidebar_aria:    Aria=Aria()
    sidebar_id:      Str="sidebar"
    sidebar_class:   Str
    sidebar_style:   Str
    sidebar_inner:   Any

Sidebar.__display__ = "Sidebar"

@optional
class Main:
    main_globals: Globals=Globals()
    main_aria:    Aria=Aria()
    main_id:      Str="main"
    main_class:   Str
    main_style:   Str
    main_inner:   Any

Main.__display__ = "Main"

@optional
class Body:
    body_globals: Globals=Globals()
    body_aria:    Aria=Aria()
    body_header:  Header
    body_footer:  Footer
    body_asides:  List(Aside)=[]
    body_main:    Main
    body_inner:   Any

Body.__display__ = "Body"

@optional
class Page:
    page_head:  Head
    page_body:  Body
    page_inner: Any

Page.__display__ = "Page"

@optional
class Column:
    col_globals: Globals=Globals()
    col_aria:    Aria=Aria()
    col_id:      Str
    col_class:   Str
    col_style:   Str
    col_inner:   Any
Col = Column

Column.__display__ = "Column"

@optional
class Row:
    row_globals: Globals=Globals()
    row_aria:    Aria=Aria()
    row_id:      Str
    row_class:   Str
    row_style:   Str
    row_cols:    List(Column)

Row.__display__ = "Row"

@optional
class Grid:
    grid_globals: Globals=Globals()
    grid_aria:    Aria=Aria()
    grid_id:      Str
    grid_class:   Str
    grid_style:   Str
    grid_rows:    List(Row)

Grid.__display__ = "Grid"
