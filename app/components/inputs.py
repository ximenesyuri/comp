from app import definer, Tag
from app.models import (
    InputText,
    InputPassword,
    InputEmail,
    InputTextArea,
    InputSearch,
)

@definer
def input_text(input: InputText) -> Tag('input'):
    return """jinja
<input
    type="{{ input['input_type'] }}"
    {% if input['input_id'] %}id="{{ input['input_id'] }}"{% endif %}
    {% if input['input_class'] %}class="{{ input['input_class'] }}"{% endif %}
    {% if input['input_placeholder'] %}placeholder="{{ input['input_placeholder'] }}"{% endif %}
    {% if input['input_value'] %}value="{{ input['input_value'] }}"{% endif %}
    {% if input['input_name'] %}name="{{ input['input_name'] }}"{% endif %}
    {% if input['input_autocomplete'] %}autocomplete="on"{% endif %}
    {% if input['input_required'] %}required{% endif %}
    {% if input['input_disabled'] %}disabled{% endif %}
    {% if input['input_readonly'] %}readonly{% endif %}
    {% if input['input_autofocus'] %}autofocus{% endif %}
    {% if input['input_tabindex'] %}tabindex="{{ input['input_tabindex'] }}"{% endif %}
    {% if input['input_form_id'] %}form="{{ input['input_form_id'] }}"{% endif %}
    {% if input['input_minlength'] %}minlength="{{ input['input_minlength'] }}"{% endif %}
    {% if input['input_maxlength'] %}maxlength="{{ input['input_maxlength'] }}"{% endif %}
    {% if input['input_pattern'] %}pattern="{{ input['input_pattern'] }}"{% endif %}
    {% if input['input_size'] %}size="{{ input['input_size'] }}"{% endif %}
>
"""

@definer
def input_search(input: InputSearch) -> Tag('input'):
    return """jinja
<input
    type="{{ input['input_type'] }}"
    {% if input['input_id'] %}id="{{ input['input_id'] }}"{% endif %}
    {% if input['input_class'] %}class="{{ input['input_class'] }}"{% endif %}
    {% if input['input_placeholder'] %}placeholder="{{ input['input_placeholder'] }}"{% endif %}
    {% if input['input_name'] %}name="{{ input['input_name'] }}"{% endif %}
    {% if input['input_autocomplete'] %}autocomplete="on"{% endif %}
    {% if input['input_required'] %}required{% endif %}
    {% if input['input_disabled'] %}disabled{% endif %}
    {% if input['input_readonly'] %}readonly{% endif %}
    {% if input['input_autofocus'] %}autofocus{% endif %}
    {% if input['input_tabindex'] %}tabindex="{{ input['input_tabindex'] }}"{% endif %}
    {% if input['input_form_id'] %}form="{{ input['input_form_id'] }}"{% endif %}
    {% if input['input_minlength'] %}minlength="{{ input['input_minlength'] }}"{% endif %}
    {% if input['input_maxlength'] %}maxlength="{{ input['input_maxlength'] }}"{% endif %}
    {% if input['input_pattern'] %}pattern="{{ input['input_pattern'] }}"{% endif %}
    {% if input['input_size'] %}size="{{ input['input_size'] }}"{% endif %}
>
"""

@definer
def input_password(input: InputPassword) -> Tag('input'):
    return """jinja
<input
    type="{{ input['input_type'] }}"
    {% if input['input_id'] %}id="{{ input['input_id'] }}"{% endif %}
    {% if input['input_class'] %}class="{{ input['input_class'] }}"{% endif %}
    {% if input['input_placeholder'] %}placeholder="{{ input['input_placeholder'] }}"{% endif %}
    {% if input['input_value'] %}value="{{ input['input_value'] }}"{% endif %}
    {% if input['input_name'] %}name="{{ input['input_name'] }}"{% endif %}
    {% if input['input_autocomplete'] %}autocomplete="on"{% endif %}
    {% if input['input_required'] %}required{% endif %}
    {% if input['input_disabled'] %}disabled{% endif %}
    {% if input['input_readonly'] %}readonly{% endif %}
    {% if input['input_autofocus'] %}autofocus{% endif %}
    {% if input['input_tabindex'] %}tabindex="{{ input['input_tabindex'] }}"{% endif %}
    {% if input['input_form_id'] %}form="{{ input['input_form_id'] }}"{% endif %}
    {% if input['input_minlength'] %}minlength="{{ input['input_minlength'] }}"{% endif %}
    {% if input['input_maxlength'] %}maxlength="{{ input['input_maxlength'] }}"{% endif %}
    {% if input['input_pattern'] %}pattern="{{ input['input_pattern'] }}"{% endif %}
    {% if input['input_size'] %}size="{{ input['input_size'] }}"{% endif %}
>
"""

@definer
def input_email(input: InputEmail) -> Tag('input'):
    return """jinja
<input
    type="{{ input['input_type'] }}"
    {% if input['input_id'] %}id="{{ input['input_id'] }}"{% endif %}
    {% if input['input_class'] %}class="{{ input['input_class'] }}"{% endif %}
    {% if input['input_placeholder'] %}placeholder="{{ input['input_placeholder'] }}"{% endif %}
    {% if input['input_value'] %}value="{{ input['input_value'] }}"{% endif %}
    {% if input['input_name'] %}name="{{ input['input_name'] }}"{% endif %}
    {% if input['input_autocomplete'] %}autocomplete="on"{% endif %}
    {% if input['input_required'] %}required{% endif %}
    {% if input['input_disabled'] %}disabled{% endif %}
    {% if input['input_readonly'] %}readonly{% endif %}
    {% if input['input_autofocus'] %}autofocus{% endif %}
    {% if input['input_tabindex'] %}tabindex="{{ input['input_tabindex'] }}"{% endif %}
    {% if input['input_form_id'] %}form="{{ input['input_form_id'] }}"{% endif %}
    {% if input['input_minlength'] %}minlength="{{ input['input_minlength'] }}"{% endif %}
    {% if input['input_maxlength'] %}maxlength="{{ input['input_maxlength'] }}"{% endif %}
    {% if input['input_pattern'] %}pattern="{{ input['input_pattern'] }}"{% endif %}
    {% if input['input_size'] %}size="{{ input['input_size'] }}"{% endif %}
    {% if input['input_multiple'] %}multiple{% endif %}
>
"""

@definer
def input_textarea(input: InputTextArea) -> Tag('textarea'):
    return """jinja
<textarea
    {% if input['input_id'] %}id="{{ input['input_id'] }}"{% endif %}
    {% if input['input_class'] %}class="{{ input['input_class'] }}"{% endif %}
    {% if input['input_placeholder'] %}placeholder="{{ input['input_placeholder'] }}"{% endif %}
    {% if input['input_name'] %}name="{{ input['input_name'] }}"{% endif %}
    {% if input['input_autocomplete'] %}autocomplete="on"{% endif %}
    {% if input['input_required'] %}required{% endif %}
    {% if input['input_disabled'] %}disabled{% endif %}
    {% if input['input_readonly'] %}readonly{% endif %}
    {% if input['input_autofocus'] %}autofocus{% endif %}
    {% if input['input_tabindex'] %}tabindex="{{ input['input_tabindex'] }}"{% endif %}
    {% if input['input_form_id'] %}form="{{ input['input_form_id'] }}"{% endif %}
    {% if input['input_rows'] %}rows="{{ input['input_rows'] }}"{% endif %}
    {% if input['input_cols'] %}cols="{{ input['input_cols'] }}"{% endif %}
    {% if input['input_wrap'] %}wrap="{{ input['input_wrap'] }}"{% endif %}
>{{ input['input_value'] }}</textarea>
"""



