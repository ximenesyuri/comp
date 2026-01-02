from utils.general import lazy

__imports__ = {
    "Aria": "comp.models.base",
    "Globals": "comp.models.base",
    "Button": "comp.models.content",
    "Icon": "comp.models.content",
    "Image": "comp.models.content",
    "Img": "comp.models.content",
    "Text": "comp.models.content",
    "Title": "comp.models.content",
    "Link": "comp.models.content",
    "Figure": "comp.models.content",
    "Logo": "comp.models.content",
    "Alpine": "comp.models.extensions",
    "HTMX": "comp.models.extensions",
    "Search": "comp.models.extensions",
    "Input": "comp.models.form",
    "Form": "comp.models.form",
    "Script": "comp.models.includes",
    "Asset": "comp.models.includes",
    "Item": "comp.models.lists",
    "Unordered": "comp.models.lists",
    "Ul": "comp.models.lists",
    "Ordered": "comp.models.lists",
    "Ol": "comp.models.lists",
    "NavItem": "comp.models.lists",
    "CustomNav": "comp.models.lists",
    "Nav": "comp.models.lists",
    "Desktop": "comp.models.responsive",
    "Tablet": "comp.models.responsive",
    "Phone": "comp.models.responsive",
    "Div": "comp.models.structure",
    "Flex": "comp.models.structure",
    "Inline": "comp.models.structure",
    "Block": "comp.models.structure",
    "Metadata": "comp.models.structure",
    "Head": "comp.models.structure",
    "Main": "comp.models.structure",
    "Body": "comp.models.structure",
    "Page": "comp.models.structure",
    "Header": "comp.models.structure",
    "Footer": "comp.models.structure",
    "Aside": "comp.models.structure",
    "Sidebar": "comp.models.structure",
    "Column": "comp.models.structure",
    "Col": "comp.models.structure",
    "Row": "comp.models.structure",
    "Grid": "comp.models.structure",
    "Markdown": "comp.models.special"
}

if lazy(__imports__):
    from comp.models.base import Aria, Globals
    from comp.models.content import Button, Icon, Image, Img, Text, Title, Link, Figure, Logo
    from comp.models.extensions import Alpine, HTMX, Search
    from comp.models.form import Input, Form
    from comp.models.includes import Script, Asset
    from comp.models.lists import Item, Unordered, Ul, Ordered, Ol, NavItem, CustomNav, Nav
    from comp.models.responsive import Desktop, Tablet, Phone
    from comp.models.structure import (
        Div, Flex, Inline, Block,
        Metadata, Head, Main, Body, Page, Header, Footer, Aside, Sidebar,
        Column, Col, Row, Grid
    )
    from comp.models.special import Markdown

