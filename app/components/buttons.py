from app.mods.factories.base import Tag
from app.mods.decorators.base import component
from app.components import button as _button
from app.models import Button, Icon
from app.components.icons.line import (
    icon_close,
    icon_menu,
    icon_search,
    icon_home,
    icon_theme_switcher
)

@component
def button_close(button: Button=Button(), icon: Icon=Icon()) -> Tag('button'):
    return (_button * icon_close)(button=button, icon=icon)

@component
def button_menu(button: Button=Button(), icon: Icon=Icon()) -> Tag('button'):
    return (_button * icon_menu)(button=button, icon=icon)

@component
def button_search(button: Button=Button(), icon: Icon=Icon()) -> Tag('button'):
    return (_button * icon_search)(button=button, icon=icon)

@component
def button_home(button: Button=Button(), icon: Icon=Icon()) -> Tag('button'):
    return (_button * icon_home)(button=button, icon=icon)

@component
def button_theme_switcher(button: Button=Button(), icon: Icon=Icon()) -> Tag('button'):
    return (_button * icon_theme_switcher)(button=button, icon=icon)
