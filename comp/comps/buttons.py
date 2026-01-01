from typed import Maybe
from comp.mods.types.base import Jinja
from comp.mods.decorators import comp
from comp.comps.content import button as _button
from comp.models import Button, Icon
from comp.mods.err import CompErr
from comp.comps.icons.line import (
    icon_close,
    icon_menu,
    icon_search,
    icon_home,
    icon_theme_switcher
)

@comp
def button_close(button: Maybe(Button)=None, icon: Maybe(Icon)=None) -> Jinja:
    try:
        if button is None:
            button = Button()
        if icon is None:
            icon = Icon()
        return (_button * icon_close)(button=button, icon=icon)
    except Exception as e:
        raise CompErr(e)

@comp
def button_menu(button: Maybe(Button)=None, icon: Maybe(Icon)=None) -> Jinja:
    try:
        if button is None:
            button = Button()
        if icon is None:
            icon = Icon()
        return (_button * icon_menu)(button=button, icon=icon)
    except Exception as e:
        raise CompErr(e)

@comp
def button_search(button: Maybe(Button)=None, icon: Maybe(Icon)=None) -> Jinja:
    try:
        if button is None:
            button = Button()
        if icon is None:
            icon = Icon()
        return (_button * icon_search)(button=button, icon=icon)
    except Exception as e:
        raise CompErr(e)

@comp
def button_home(button: Maybe(Button)=None, icon: Maybe(Icon)=None) -> Jinja:
    try:
        if button is None:
            button = Button()
        if icon is None:
            icon = Icon()
        return (_button * icon_home)(button=button, icon=icon)
    except Exception as e:
        raise CompErr(e)

@comp
def button_theme_switcher(button: Maybe(Button)=None, icon: Maybe(Icon)=None) -> Jinja:
    try:
        if button is None:
            button = Button()
        if icon is None:
            icon = Icon()
        return (_button * icon_theme_switcher)(button=button, icon=icon)
    except Exception as e:
        raise CompErr(e)
