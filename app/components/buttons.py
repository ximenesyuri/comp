from app.mods.factories.base import Tag
from app.mods.decorators.base import component
from app.components import button
from app.models import Button, Icon
from app.components.icons.line import (
    icon_close,
    icon_menu,
    icon_search,
    icon_home,
    icon_theme_switcher
)

@component
def button_close(button_data: Button=Button(), icon_data: Icon=Icon()) -> Tag('button'):
    return (button * icon_close)(button=button_data, icon=icon_data)

@component
def button_menu(button_data: Button=Button(), icon_data: Icon=Icon()) -> Tag('button'):
    return (button * icon_menu)(button=button_data, icon=icon_data)

@component
def button_search(button_data: Button=Button(), icon_data: Icon=Icon()) -> Tag('button'):
    return (button * icon_search)(button=button_data, icon=icon_data)

@component
def button_home(button_data: Button=Button(), icon_data: Icon=Icon()) -> Tag('button'):
    return (button * icon_home)(button=button_data, icon=icon_data)

@component
def button_theme_switcher(button_data: Button=Button(), icon_data: Icon=Icon()) -> Tag('button'):
    return (button * icon_theme_switcher)(button=button_data, icon=icon_data)
