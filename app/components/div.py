from typed import null
from app import definer, Jinja, jinja, Component, TagStr
from app.models import Div, Alpine
from app.nill import nill_jinja
from app.service import render

@definer
def div(div: Div=null(Div), alpine: Alpine=null(Alpine), inner: Jinja=nill_jinja) -> TagStr('div'):
    return """jinja
<div{%if div['id']%} id="{{div['id']}}"{%endif %}{%if div['classes']%} class="{{div['classes']}}"{%endif%}{%if div['hover']%} hover="{{div['hover']}}"{%endif%}{%if alpine['x_init']%} x-init="{{alpine['x_init']}}"{%endif%}{%if alpine['x_show']%} x-show="{{alpine['x_show']}}"{%endif%}{%if alpine['x_data']%} x-data="{{alpine['x_data']}}"{%endif%}{%if alpine['x_cloak']%} x-cloak{%endif%}>
    {{inner}}
</div>
"""
