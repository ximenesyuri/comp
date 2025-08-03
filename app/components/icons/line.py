from typed import typed, Str, null
from app.mods.factories.base import Tag
from app.mods.decorators.base import component
from app.models import Icon

@component
def icon_search(icon: Icon=null(Icon)) -> Tag('svg'):
    return f"""jinja
<svg
    xmlns="http://www.w3.org/2000/svg"
    [% if icon.icon_viewbox %]viewBox="{ icon.icon_viewbox }"[% endif %]
    [% if icon.icon_size %]width="{ icon.icon_size }"[% endif %]
    [% if icon.icon_size %]height="{ icon.icon_size }"[% endif %]
    [% if icon.icon_fill %]fill="{ icon.icon_fill }"[% endif %]
    [% if icon.icon_class %]class="{ icon.icon_class }"[% endif %]
> 
<path d="M784-120 532-372q-30 24-69 38t-83 14q-109 0-184.5-75.5T120-580q0-109 75.5-184.5T380-840q109 0 184.5 75.5T640-580q0 44-14 83t-38 69l252 252-56 56ZM380-400q75 0 127.5-52.5T560-580q0-75-52.5-127.5T380-760q-75 0-127.5 52.5T200-580q0 75 52.5 127.5T380-400Z"/>
</svg>
"""

@component
def icon_menu(icon: Icon=null(Icon)) -> Tag('svg'):
    return f"""jinja
<svg
    xmlns="http://www.w3.org/2000/svg"
    [% if icon.icon_viewbox %]viewBox="{ icon.icon_viewbox }"[% endif %]
    [% if icon.icon_size %]width="{ icon.icon_size }"[% endif %]
    [% if icon.icon_size %]height="{ icon.icon_size }"[% endif %]
    [% if icon.icon_fill %]fill="{ icon.icon_fill }"[% endif %]
    [% if icon.icon_class %]class="{ icon.icon_class }"[% endif %]
>
<path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z"/>
</svg>
"""

@component
def icon_close(icon: Icon=null(Icon)) -> Tag('svg'):
    return f"""jinja
<svg
    xmlns="http://www.w3.org/2000/svg"
    [% if icon.icon_viewbox %]viewBox="{ icon.icon_viewbox }"[% endif %]
    [% if icon.icon_size %]width="{ icon.icon_size }"[% endif %]
    [% if icon.icon_size %]height="{ icon.icon_size }"[% endif %]
    [% if icon.icon_fill %]fill="{ icon.icon_fill }"[% endif %]
    [% if icon.icon_class %]class="{ icon.icon_class }"[% endif %]
>
<path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/>
</svg>
"""

@component
def icon_home(icon: Icon=null(Icon)) -> Tag('svg'):
    return f"""jinja
<svg
    xmlns="http://www.w3.org/2000/svg"
    [% if icon.icon_viewbox %]viewBox="{ icon.icon_viewbox }"[% endif %]
    [% if icon.icon_size %]width="{ icon.icon_size }"[% endif %]
    [% if icon.icon_size %]height="{ icon.icon_size }"[% endif %]
    [% if icon.icon_fill %]fill="{ icon.icon_fill }"[% endif %]
    [% if icon.icon_class %]class="{ icon.icon_class }"[% endif %]
>
<path d="M240-200h120v-240h240v240h120v-360L480-740 240-560v360Zm-80 80v-480l320-240 320 240v480H520v-240h-80v240H160Zm320-350Z"/>
</svg>
"""

@component
def icon_theme_switcher(icon: Icon=null(Icon)) -> Tag('svg'):
    return f"""jinja
<svg
    xmlns="http://www.w3.org/2000/svg"
    [% if icon.icon_viewbox %]viewBox="{ icon.icon_viewbox }"[% endif %]
    [% if icon.icon_size %]width="{ icon.icon_size }"[% endif %]
    [% if icon.icon_size %]height="{ icon.icon_size }"[% endif %]
    [% if icon.icon_fill %]fill="{ icon.icon_fill }"[% endif %]
    [% if icon.icon_class %]class="{ icon.icon_class }"[% endif %]
>
<path d="M396-396q-32-32-58.5-67T289-537q-5 14-6.5 28.5T281-480q0 83 58 141t141 58q14 0 28.5-2t28.5-6q-39-22-74-48.5T396-396Zm57-56q51 51 114 87.5T702-308q-40 51-98 79.5T481-200q-117 0-198.5-81.5T201-480q0-65 28.5-123t79.5-98q20 72 56.5 135T453-452Zm290 72q-20-5-39.5-11T665-405q8-18 11.5-36.5T680-480q0-83-58.5-141.5T480-680q-20 0-38.5 3.5T405-665q-8-19-13.5-38T381-742q24-9 49-13.5t51-4.5q117 0 198.5 81.5T761-480q0 26-4.5 51T743-380ZM440-840v-120h80v120h-80Zm0 840v-120h80V0h-80Zm323-706-57-57 85-84 57 56-85 85ZM169-113l-57-56 85-85 57 57-85 84Zm671-327v-80h120v80H840ZM0-440v-80h120v80H0Zm791 328-85-85 57-57 84 85-56 57ZM197-706l-84-85 56-57 85 85-57 57Zm199 310Z"/>
</svg>
"""
