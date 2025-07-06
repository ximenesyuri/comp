from typed import null
from app import definer, Div, Button
from app.models import ElementModel, AlpineModel, ButtonModel
from app.nill import nill_jinja

@definer
def div(div: ElementModel=null(ElementModel), alpine: AlpineModel=null(AlpineModel)) -> Div:
    return """jinja
<div{%if div.id %} id="{{ div.id }}"{%endif %}{%if div.classes%} class="{{div.classes}}"{%endif%}{%if div.hover%} hover="{{div.hover}}"{%endif%}{%if alpine['x_init']%} x-init="{{alpine['x_init']}}"{%endif%}{%if alpine['x_show']%} x-show="{{alpine['x_show']}}"{%endif%}{%if alpine['x_data']%} x-data="{{alpine['x_data']}}"{%endif%}{%if alpine['x_cloak']%} x-cloak{%endif%}>
    {{inner}}
</div>
"""

@definer
def button(b: ButtonModel=null(ButtonModel)) -> Button:
    return """jinja
<button 
    {%if b['id']%}id="{{b['id']}}"{%endif%}
    {%if b['classes']%}class="{{b['classes']}}"{%endif%}
    {%if b['hover']%}class="{{b['hover']}}"{%endif%}
    type="button"
    {%if b['on_click']%}@click="{{b['on_click']}}"{%endif%}
    {%if b['click_away']%}@click="{{b['click_away']}}"{%endif%}
>       
    {{button_inner}}
</button>
"""
