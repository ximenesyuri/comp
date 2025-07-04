import re
from typed import typed, Str, List, Tuple, Dict, Any
from inspect import signature, Parameter, getmodule
from jinja2 import Environment, DictLoader, StrictUndefined
from app.mods.helper import _jinja_regex, _get_variables_map, _find_jinja_vars, _definer
from app.mods.factories import FreeDefiner
from app.mods.types import Definer, Jinja

@typed
def concat(free_definer: FreeDefiner(1), definer_: Definer) -> Definer:
    """
    Concatenates a 'FreeDefiner(1)' definer with another definer.
        1. The 'free' must have exactly one free variable.
        2. If 'free' has parameters '(y1 ..., free_var)' and
          'definer' has parameters '(x1, ...)', then `concat` will have
           parameters '(y1,..., x1, ...)'.
        3. 'depends_on' of the concatenation is the concatenation of
          the 'depends_on'. The free variable is treated as a slot.
          Common parameters between free_definer and definer_ are merged,
          with 'definer_' taking precedence for type and default if common.
    """
    sig_free = signature(getattr(free_definer, 'func', free_definer))
    free_params: Dict[str, Parameter] = {p.name:p for p in sig_free.parameters.values() if p.name != "depends_on"}

    free_kwargs_for_raw_template = {k: f"{{{{ {k} }}}}" for k in free_params.keys()}
    if "depends_on" in sig_free.parameters:
        free_kwargs_for_raw_template["depends_on"] = []

    jinja_src_free_definer_raw = free_definer(**free_kwargs_for_raw_template)

    vars_in_template = _find_jinja_vars(jinja_src_free_definer_raw)
    free_template_vars = vars_in_template - set(free_params.keys())

    if len(free_template_vars) != 1:
        raise ValueError(f"FreeDefiner for concat must have exactly one free variable in its template "
                         f"that is not one of its function arguments. Found: {free_template_vars}")
    free_var = next(iter(free_template_vars))

    sig_def = signature(getattr(definer_, 'func', definer_))
    def_params = {p.name:p for p in sig_def.parameters.values() if p.name != "depends_on"}

    combined_params_dict = {}
    for name, param in free_params.items():
        if name != free_var:
            combined_params_dict[name] = param
    for name, param in def_params.items():
        combined_params_dict[name] = param

    new_params_final = list(combined_params_dict.values())
    combined_depends_on = []
    if 'depends_on' in sig_free.parameters and sig_free.parameters['depends_on'].default is not Parameter.empty:
        combined_depends_on.extend(list(sig_free.parameters['depends_on'].default))
    if 'depends_on' in sig_def.parameters and sig_def.parameters['depends_on'].default is not Parameter.empty:
        combined_depends_on.extend(list(sig_def.parameters['depends_on'].default))
    if combined_depends_on:
        combined_depends_on = sorted(list(set(combined_depends_on)), key=lambda x: getattr(x, '__name__', str(x)))
        depends_on_param = Parameter(
            "depends_on", Parameter.KEYWORD_ONLY, default=combined_depends_on, annotation=List(Definer)
        )
        new_params_final.append(depends_on_param)

    def_kwargs_for_raw = {k: f"{{{{ {k} }}}}" for k in def_params.keys()}
    if "depends_on" in sig_def.parameters:
        def_kwargs_for_raw['depends_on'] = []

    jinja_src_definer_raw = definer_(**def_kwargs_for_raw)

    m_def = re.match(_jinja_regex(), jinja_src_definer_raw, re.DOTALL)
    if not m_def:
        raise ValueError("definer_ did not return a valid Jinja template for raw extraction.")
    def_jinja_content_raw = m_def.group(1)

    m_free = re.match(_jinja_regex(), jinja_src_free_definer_raw, re.DOTALL)
    if not m_free:
        raise ValueError("free_definer did not return a valid Jinja template for raw extraction.")
    free_jinja_content_raw_template = m_free.group(1)

    free_var_re = r"(\{\{\s*" + re.escape(free_var) + r"\s*\}\})"
    combined_raw_jinja_content = re.sub(free_var_re, def_jinja_content_raw, free_jinja_content_raw_template, count=1)

    _concat_target_signature = signature(lambda: None).replace(parameters=new_params_final)

    def _concat_definer_logic(*args, **kwargs_in) -> Jinja:
        try:
            bound_args = _concat_target_signature.bind(*args, **kwargs_in)
            bound_args.apply_defaults()
            all_combined_kwargs = bound_args.arguments
        except TypeError as e:
            raise TypeError(f"Error binding arguments for concat definer: {e}")

        current_depends_on = all_combined_kwargs.pop("depends_on", combined_depends_on)
        free_definer_call_kwargs = {}
        for name, param in sig_free.parameters.items():
            if name == "depends_on":
                free_definer_call_kwargs[name] = current_depends_on
            elif name == free_var:
                pass
            elif name in all_combined_kwargs:
                free_definer_call_kwargs[name] = all_combined_kwargs[name]
            elif param.default is not Parameter.empty:
                free_definer_call_kwargs[name] = param.default
            else:
                raise TypeError(f"Missing argument '{name}' for free_definer in concat during execution.")

        definer_call_kwargs = {}
        for name, param in sig_def.parameters.items():
            if name == "depends_on":
                definer_call_kwargs[name] = current_depends_on
            elif name in all_combined_kwargs:
                definer_call_kwargs[name] = all_combined_kwargs[name]
                # If a shared parameter, it implicitly takes the value from bound_args
            elif param.default is not Parameter.empty:
                definer_call_kwargs[name] = param.default
            else:
                raise TypeError(f"Missing argument '{name}' for definer_ in concat during execution.")

        def_rendered_output_jinja = definer_(**definer_call_kwargs)
        m_def_rendered = re.match(_jinja_regex(), def_rendered_output_jinja, re.DOTALL)
        if not m_def_rendered:
            raise ValueError("definer_ did not return a valid Jinja template during execution.")
        def_jinja_content_rendered = m_def_rendered.group(1)

        free_definer_call_kwargs[free_var] = def_jinja_content_rendered
        free_definer_to_call = getattr(free_definer, 'func', free_definer) # Handle typed wrappers
        free_rendered_output_jinja = free_definer_to_call(**free_definer_call_kwargs)
        m_free_rendered = re.match(_jinja_regex(), free_rendered_output_jinja, re.DOTALL)
        if not m_free_rendered:
            raise ValueError("free_definer did not return a valid Jinja template during final rendering.")
        final_jinja_content = m_free_rendered.group(1)

        return "jinja\n" + final_jinja_content

    _concat_definer_logic.__name__ = f"concat_{getattr(free_definer, '__name__', 'anon')}_with_{getattr(definer_, '__name__','anon')}"
    _concat_definer_logic.__annotations__ = {p.name:p.annotation for p in new_params_final if p.annotation is not Parameter.empty}
    _concat_definer_logic.__annotations__['return'] = Jinja
    _concat_definer_logic.__signature__ = _concat_target_signature

    wrapped_definer = _definer(_concat_definer_logic)
    wrapped_definer._is_dynamic_definer = True
    wrapped_definer._raw_combined_jinja = combined_raw_jinja_content

    return wrapped_definer

@typed
def join(*definers: Tuple(Definer)) -> Definer:
    """
    Receives a list of definers and creates a new definer whose jinja string
    is the sum (concatenation) of the given jinja strings.
    The new definer's signature will be the union of all unique parameters
    from the input definers. If a parameter exists in multiple definers with
    different types, the last one encountered will be used. Default values from
    the latest encountered definer for a given parameter name will be used.
    'depends_on' arguments are merged.
    """
    if not definers:
        @_definer
        def empty_join() -> Jinja:
            return "jinja\n"
        empty_join._is_dynamic_definer = True
        empty_join._raw_combined_jinja = ""
        return empty_join

    combined_params_dict = {}
    combined_depends_on = []

    for d in definers:
        sig = signature(getattr(d, 'func', d))
        for name, param in sig.parameters.items():
            if name == "depends_on":
                if param.default is not Parameter.empty and isinstance(param.default, list):
                    combined_depends_on.extend(param.default)
            else:
                combined_params_dict[name] = param

    new_parameters = list(combined_params_dict.values())

    if combined_depends_on:
        combined_depends_on = sorted(list(set(combined_depends_on)), key=lambda x: getattr(x, '__name__', str(x)))
        depends_on_param = Parameter(
            "depends_on",
            Parameter.KEYWORD_ONLY,
            default=combined_depends_on,
            annotation=List(Definer)
        )
        new_parameters.append(depends_on_param)

    annotations = {p.name: p.annotation for p in new_parameters if p.annotation is not Parameter.empty}
    annotations['return'] = Jinja

    accumulated_raw_jinja_content = ""
    for d in definers:
        sub_definer_raw_jinja = d.jinja
        accumulated_raw_jinja_content += sub_definer_raw_jinja

    _joined_target_signature = signature(lambda: None).replace(parameters=new_parameters)

    def _joined_definer_logic(*args, **kwargs_in) -> Jinja:
        try:
            bound_args = _joined_target_signature.bind(*args, **kwargs_in)
            bound_args.apply_defaults()
            kwargs = bound_args.arguments
        except TypeError as e:
            raise TypeError(f"Error binding arguments for joined definer: {e}")

        current_depends_on = kwargs.pop("depends_on", [])
        combined_jinja_parts_to_render = ""

        for d in definers:
            d_sig = signature(getattr(d, 'func', d))
            d_kwargs = {}
            for name, param in d_sig.parameters.items():
                if name == "depends_on":
                    d_kwargs[name] = current_depends_on
                elif name in kwargs:
                    d_kwargs[name] = kwargs[name]
                elif param.default is not Parameter.empty:
                    d_kwargs[name] = param.default
                else:
                    raise TypeError(f"Missing required argument '{name}' for definer '{getattr(d, '__name__', 'anonymous')}' during join operation.")
            try:
                jinja_str_from_sub_definer = d(**d_kwargs)
            except Exception as e:
                raise RuntimeError(f"Error calling definer {getattr(d, '__name__', 'anonymous')} during join: {e}")

            match = re.match(_jinja_regex(), jinja_str_from_sub_definer, re.DOTALL)
            if not match:
                raise ValueError(f"Definer {getattr(d, '__name__', 'anonymous')} did not return a valid Jinja string during execution.")
            combined_jinja_parts_to_render += match.group(1)

        return "jinja\n" + combined_jinja_parts_to_render

    joined_func_name = f"joined_{'_'.join(getattr(d, '__name__', 'anon') for d in definers)}"

    _joined_definer_logic.__name__ = joined_func_name
    _joined_definer_logic.__annotations__ = annotations
    _joined_definer_logic.__module__ = __name__
    _joined_definer_logic.__signature__ = _joined_target_signature
    wrapped_definer = _definer(_joined_definer_logic)
    wrapped_definer._is_dynamic_definer = True
    wrapped_definer._raw_combined_jinja = accumulated_raw_jinja_content
    return wrapped_definer
