from typed import null
from app import definer, Tag
from app.models import Div, Alpine, Button
from app.nill import nill_jinja

@definer
def div(div: Div=null(Div), alpine: Alpine=null(Alpine)) -> Tag('div'):
    return """jinja
<div
    {%if div['div_id'] %}id="{{ div['div_id'] }}"{%endif %}
    {%if div['div_class']%}class="{{div['div_class']}}"{%endif%}
    {%if div['div_hover']%}hover="{{div['div_hover']}}"{%endif%}
    {%if alpine['x_init']%}x-init="{{alpine['x_init']}}"{%endif%}
    {%if alpine['x_show']%}x-show="{{alpine['x_show']}}"{%endif%}
    {%if alpine['x_data']%}x-data="{{alpine['x_data']}}"{%endif%}
    {%if alpine['x_cloak']%}x-cloak{%endif%}
>
    {{div_inner}}
</div>
"""

@definer
def button(button: Button=null(Button)) -> Tag('button'):
    return """jinja
<button 
    {%if button['button_id']%}id="{{button['button_id']}}"{%endif%}
    {%if button['button_class']%}class="{{button['button_class']}}"{%endif%}
    {%if button['button_hover']%}hover="{{button['button_hover']}}"{%endif%}
    type="button"
    {%if button['on_click']%}@click="{{button['on_click']}}"{%endif%}
    {%if button['click_away']%}@click_away="{{button['click_away']}}"{%endif%}
>       
    {{button_inner}}
</button>
"""
