from app import definer
from app.models import Div, Button, Alpine
from app.components import div

@definer
def base(div: Div, button: Button, alpine: Alpine) -> Jinja:
    return """jinja
<div {% if x_show %}x-show="{{x_show}}"{% endif %} id="{{div_id}}" class="{{div_class}}">
    <button
        id="{{ button_id }}"
        class="{{ button_class }}"
        hover="{{ button_hover }}"
        type="button"
        {% if on_click %}@click="{{on_click}}"{% endif %}
        {% if click_away %}@click_away="{{click_away}}"{% endif %}
    >       
        {{button_content}}
    </button>
</div>
"""
