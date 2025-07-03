import re
from typed import typed, Str, List, Tuple, Dict, Any
from inspect import signature, Parameter, getmodule
from app.mods.helper import _jinja_regex, _get_variables_map, _find_jinja_vars, _definer
from app.mods.factories import FreeDefiner
from app.mods.types import Definer, Jinja

@typed
def jinja(jinjastr: Jinja) -> Str:
    """
    Extract the jinja content of a jinja string.
    """
    regex_str = re.compile(_jinja_regex(), re.DOTALL)
    match = regex_str.match(jinjastr)
    if match:
        return match.group(1)
    return ""

@typed
def concat(free_definer: FreeDefiner(1), definer_: Definer) -> Definer:
    """
    Concatenates a 'FreeDefiner(1)' definer with another definer.
        1. The 'free' must have exactly one free variable.
        2. If 'free' has parameters '(y1 ..., free_var)' and
          'definer' has parameters '(x1, ...)', then `concat` will have
           parameters '(y1,..., x1, ...)'.
        3. None 'x1,...' should be named 'free_var'
          'concat(y1,...,x1,...)'is obtained by replacing '{{ free_var }}'
           inside 'free(y1,...,free_var)' with 'definer(x1,...)'.
        4. 'depends_on' of the concatenation is the concatenation of
          the 'depends_on'.
    """
    sig_free = signature(getattr(free_definer, 'func', free_definer))
    free_params: Dict[str, Parameter] = {p.name:p for p in sig_free.parameters.values() if p.name != "depends_on"}
    free_param_names = set(free_params.keys())

    # Introspect Jinja variables: only pass declared params
    dummy_kwargs = {k: "dummy" for k in free_param_names}
    if "depends_on" in sig_free.parameters:
        dummy_kwargs["depends_on"] = []
    jinja_src = free_definer(**dummy_kwargs)
    vars_in_template = _find_jinja_vars(jinja_src)
    free_template_vars = vars_in_template - free_param_names
    if len(free_template_vars) != 1:
        raise ValueError(f"FreeDefiner must have exactly one free variable, found: {free_template_vars}")
    free_var = next(iter(free_template_vars))

    sig_def = signature(getattr(definer_, 'func', definer_))
    def_params: Dict[str, Parameter] = {p.name:p for p in sig_def.parameters.values() if p.name != "depends_on"}
    def_param_names = set(def_params.keys())

    overlapped = (free_param_names & def_param_names)
    if overlapped:
        raise ValueError(f"Parameter name overlap between free definer and concat'd definer: {overlapped}")

    ordered_params = []
    for name in sig_free.parameters:
        if name=="depends_on": continue
        if name==free_var: continue
        ordered_params.append(free_params[name])
    for name in sig_def.parameters:
        if name=="depends_on": continue
        ordered_params.append(def_params[name])

    # Compute combined depends_on
    combined_depends_on = []
    if 'depends_on' in sig_free.parameters and sig_free.parameters['depends_on'].default is not Parameter.empty:
        combined_depends_on += list(sig_free.parameters['depends_on'].default)
    if 'depends_on' in sig_def.parameters and sig_def.parameters['depends_on'].default is not Parameter.empty:
        combined_depends_on += list(sig_def.parameters['depends_on'].default)
    depends_on_param = Parameter("depends_on", Parameter.KEYWORD_ONLY, default=combined_depends_on, annotation=List(Definer))
    new_params_final = ordered_params + [depends_on_param]

    def concat_definer(**kwargs):
        depends_on = kwargs.pop("depends_on", combined_depends_on)
        # The parameters for free_definer: only formal params (except the free var itself).
        free_kwargs = {name:kwargs[name] for name in free_param_names if name != free_var and name in kwargs}
        if "depends_on" in sig_free.parameters:
            free_kwargs['depends_on'] = depends_on
        # Only set free_var if it's declared as a param (very rare!), not for free variable slot sub.
        if free_var in free_param_names:
            free_kwargs[free_var] = "__MAGIC_PLACEHOLDER__"

        free_rendered = free_definer(**free_kwargs)
        m = re.match(_jinja_regex(), free_rendered, re.DOTALL)
        if not m:
            raise ValueError("free_definer did not return a valid Jinja template.")
        free_jinja = m.group(1)

        # Prepare definer_ params: only pass those it actually wants.
        def_kwargs = {name:kwargs[name] for name in def_param_names if name in kwargs}
        if "depends_on" in sig_def.parameters:
            def_kwargs['depends_on'] = depends_on
        def_rendered = definer_(**def_kwargs)
        m2 = re.match(_jinja_regex(), def_rendered, re.DOTALL)
        if not m2:
            raise ValueError("definer_ did not return a valid Jinja template.")
        def_jinja = m2.group(1)

        # Replace the *template slot* ({{ free_var }}) with def_jinja
        free_var_re = r"(\{\{\s*" + re.escape(free_var) + r"\s*\}\})"
        new_jinja = re.sub(free_var_re, def_jinja, free_jinja, count=1)

        return "jinja\n" + new_jinja

    concat_definer.__name__ = f"concat_{getattr(free_definer, '__name__', 'anon')}_with_{getattr(definer_, '__name__','anon')}"
    concat_definer.__annotations__ = {p.name:p.annotation for p in new_params_final if p.annotation is not Parameter.empty}
    concat_definer.__annotations__['return'] = Jinja

    from functools import wraps
    concat_signature = signature(lambda **kwargs: None).replace(parameters=new_params_final)
    @wraps(concat_definer)
    def concat_forwarder(*args, **kwargs):
        bound = concat_signature.bind(*args, **kwargs)
        return concat_definer(**bound.arguments)
    concat_forwarder.__signature__ = concat_signature
    concat_forwarder.__annotations__ = concat_definer.__annotations__
    concat_forwarder.__name__ = concat_definer.__name__

    return _definer(concat_forwarder) 
