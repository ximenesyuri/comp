from app.mods.factories.base import Tag
from app.mods.decorators.base import component
from app.models import (
    InputText,
    InputPass,
    InputEmail,
    InputTextArea,
    InputSearch,
)

@component
def input_text(input: InputText=InputText()) -> Tag('input'):
    return f"""jinja
<input
    type="{ input.input_type }"
    [% if input.input_id %]id="{ input.input_id }"[% endif %]
    [% if input.input_class %]class="{ input.input_class }"[% endif %]
    [% if input.input_placeholder %]placeholder="{ input.input_placeholder }"[% endif %]
    [% if input.input_value %]value="{ input.input_value }"[% endif %]
    [% if input.input_name %]name="{ input.input_name }"[% endif %]
    [% if input.input_autocomplete %]autocomplete="on"[% endif %]
    [% if input.input_required %]required[% endif %]
    [% if input.input_disabled %]disabled[% endif %]
    [% if input.input_readonly %]readonly[% endif %]
    [% if input.input_autofocus %]autofocus[% endif %]
    [% if input.input_tabindex %]tabindex="{ input.input_tabindex }"[% endif %]
    [% if input.input_form_id %]form="{ input.input_form_id }"[% endif %]
    [% if input.input_minlength %]minlength="{ input.input_minlength }"[% endif %]
    [% if input.input_maxlength %]maxlength="{ input.input_maxlength }"[% endif %]
    [% if input.input_pattern %]pattern="{ input.input_pattern }"[% endif %]
    [% if input.input_size %]size="{ input.input_size }"[% endif %]
>
"""

@component
def input_search(input: InputSearch=InputSearch()) -> Tag('input'):
    return f"""jinja
<input
    type="{ input.input_type }"
    [% if input.input_id %]id="{ input.input_id }"[% endif %]
    [% if input.input_class %]class="{ input.input_class }"[% endif %]
    [% if input.input_placeholder %]placeholder="{ input.input_placeholder }"[% endif %]
    [% if input.input_value %]value="{ input.input_value }"[% endif %]
    [% if input.input_name %]name="{ input.input_name }"[% endif %]
    [% if input.input_autocomplete %]autocomplete="on"[% endif %]
    [% if input.input_required %]required[% endif %]
    [% if input.input_disabled %]disabled[% endif %]
    [% if input.input_readonly %]readonly[% endif %]
    [% if input.input_autofocus %]autofocus[% endif %]
    [% if input.input_tabindex %]tabindex="{ input.input_tabindex }"[% endif %]
    [% if input.input_form_id %]form="{ input.input_form_id }"[% endif %]
    [% if input.input_minlength %]minlength="{ input.input_minlength }"[% endif %]
    [% if input.input_maxlength %]maxlength="{ input.input_maxlength }"[% endif %]
    [% if input.input_pattern %]pattern="{ input.input_pattern }"[% endif %]
    [% if input.input_size %]size="{ input.input_size }"[% endif %]
>
"""

@component
def input_pass(input: InputPass=InputPass()) -> Tag('input'):
    return f"""jinja
<input
    type="{ input.input_type }"
    [% if input.input_id %]id="{ input.input_id }"[% endif %]
    [% if input.input_class %]class="{ input.input_class }"[% endif %]
    [% if input.input_placeholder %]placeholder="{ input.input_placeholder }"[% endif %]
    [% if input.input_value %]value="{ input.input_value }"[% endif %]
    [% if input.input_name %]name="{ input.input_name }"[% endif %]
    [% if input.input_autocomplete %]autocomplete="on"[% endif %]
    [% if input.input_required %]required[% endif %]
    [% if input.input_disabled %]disabled[% endif %]
    [% if input.input_readonly %]readonly[% endif %]
    [% if input.input_autofocus %]autofocus[% endif %]
    [% if input.input_tabindex %]tabindex="{ input.input_tabindex }"[% endif %]
    [% if input.input_form_id %]form="{ input.input_form_id }"[% endif %]
    [% if input.input_minlength %]minlength="{ input.input_minlength }"[% endif %]
    [% if input.input_maxlength %]maxlength="{ input.input_maxlength }"[% endif %]
    [% if input.input_pattern %]pattern="{ input.input_pattern }"[% endif %]
    [% if input.input_size %]size="{ input.input_size }"[% endif %]
>
"""

@component
def input_email(input: InputEmail=InputEmail()) -> Tag('input'):
    return f"""jinja
<input
    type="{ input.input_type }"
    [% if input.input_id %]id="{ input.input_id }"[% endif %]
    [% if input.input_class %]class="{ input.input_class }"[% endif %]
    [% if input.input_placeholder %]placeholder="{ input.input_placeholder }"[% endif %]
    [% if input.input_value %]value="{ input.input_value }"[% endif %]
    [% if input.input_name %]name="{ input.input_name }"[% endif %]
    [% if input.input_autocomplete %]autocomplete="on"[% endif %]
    [% if input.input_required %]required[% endif %]
    [% if input.input_disabled %]disabled[% endif %]
    [% if input.input_readonly %]readonly[% endif %]
    [% if input.input_autofocus %]autofocus[% endif %]
    [% if input.input_tabindex %]tabindex="{ input.input_tabindex }"[% endif %]
    [% if input.input_form_id %]form="{ input.input_form_id }"[% endif %]
    [% if input.input_minlength %]minlength="{ input.input_minlength }"[% endif %]
    [% if input.input_maxlength %]maxlength="{ input.input_maxlength }"[% endif %]
    [% if input.input_pattern %]pattern="{ input.input_pattern }"[% endif %]
    [% if input.input_size %]size="{ input.input_size }"[% endif %]
>
"""

@component
def input_textarea(input: InputTextArea=InputTextArea()) -> Tag('textarea'):
    return f"""jinja
<textarea
    [% if input.input_id %]id="{ input.input_id }"[% endif %]
    [% if input.input_class %]class="{ input.input_class }"[% endif %]
    [% if input.input_placeholder %]placeholder="{ input.input_placeholder }"[% endif %]
    [% if input.input_value %]value="{ input.input_value }"[% endif %]
    [% if input.input_name %]name="{ input.input_name }"[% endif %]
    [% if input.input_autocomplete %]autocomplete="on"[% endif %]
    [% if input.input_required %]required[% endif %]
    [% if input.input_disabled %]disabled[% endif %]
    [% if input.input_readonly %]readonly[% endif %]
    [% if input.input_autofocus %]autofocus[% endif %]
    [% if input.input_tabindex %]tabindex="{ input.input_tabindex }"[% endif %]
    [% if input.input_form_id %]form="{ input.input_form_id }"[% endif %]
    [% if input.input_minlength %]minlength="{ input.input_minlength }"[% endif %]
    [% if input.input_maxlength %]maxlength="{ input.input_maxlength }"[% endif %]
    [% if input.input_pattern %]pattern="{ input.input_pattern }"[% endif %]
    [% if input.input_size %]size="{ input.input_size }"[% endif %] 
>{ input.input_value }</textarea>
"""
