import re
from inspect import signature, getsource
from jinja2 import Environment, meta
from typed import typed, Str, Json, Bool, Union, Extension, Path, TypedFuncType
from typed.models import model, conditional, Optional
from typed.more import Markdown
from app.mods.types.meta import _DEFINER
from app.mods.decorators.definer import definer

class DEFINER(_DEFINER('Definer', (TypedFuncType,), {})):
    @property
    def jinja(self):
        """
        Returns the Jinja string of the definer.
        For static definers, it parses the source.
        For dynamic definers created by `join` or `concat`, it returns the pre-combined raw Jinja template.
        """
        if hasattr(self, '_is_dynamic_definer') and self._is_dynamic_definer:
            if hasattr(self, '_raw_combined_jinja'):
                return self._raw_combined_jinja
            else:
                print(f"Warning: Dynamic definer {self.__name__} is missing _raw_combined_jinja attribute.")
                return ""
        else:
            code = getsource(self)
            regex_str = re.compile(r"\"\"\"jinja([\s\S]*?)\"\"\"", re.DOTALL)
            match = regex_str.search(code)
            if match:
                return match.group(1)
            return ""

    @property
    def args(self):
        return tuple(signature(self).parameters.keys())

    @property
    def jinja_vars(self):
        """
        Returns the tuple of all Jinja variables found in the definer's template.
        Uses _find_jinja_vars.
        """
        env = Environment()
        jinja_content = self.jinja
        if not jinja_content:
            return ()
        ast = env.parse(jinja_content)
        return tuple(sorted(meta.find_undeclared_variables(ast)))

    @property
    def jinja_free_vars(self):
        """Returns the tuple of free Jinja variables (not corresponding to arguments)."""
        all_vars = set(self.jinja_vars)
        arg_vars = set(self.args)
        arg_vars.discard("depends_on")
        return tuple(sorted(list(all_vars - arg_vars)))

    def __add__(self, other):
        """
        Implements definer_1 + definer_2 => join(definer_1, definer_2)
        """
        if not isinstance(other, DEFINER):
            return NotImplemented
        from app.mods.functions import join
        return join(self, other)

    def __mul__(self, other):
        """
        Implements definer_1 * definer_2 => concat(definer_1, definer_2)
        Here, definer_1 is assumed to be the 'free_definer' with a single free variable slot,
        and definer_2 is the content to fill that slot.
        """
        if not isinstance(other, DEFINER):
            return NotImplemented
        from app.mods.decorators.definer import _FREE_DEFINER_REGISTRY
        InstanceFree = _FREE_DEFINER_REGISTRY.get('__FreeInstance__')
        if InstanceFree is None:
            from app.mods.factories.base import Definer
            InstanceFree = Definer(1)
            _FREE_DEFINER_REGISTRY['__FreeInstance__'] = InstanceFree

        if not isinstance(self, InstanceFree):
            raise TypeError(
                f"The left operand of '*' (i.e., '{self.__name__}') must be a Definer with "
                "exactly one free Jinja variable to be used with concat (Free(1)).\n"
                f"Its free variables are: {self.jinja_free_vars}"
            )

        from app.mods.functions import concat
        return concat(self, other)

@model
class _COMPONENT:
    definer: DEFINER
    context: Json

@typed
def _check_context(component: _COMPONENT) -> Bool:
    definer = component.get('definer')
    context = component.get('context', {})
    if not isinstance(context, dict):
        context = {}

    local_vars = getattr(definer, "_local_vars", set())
    for var in local_vars:
        if var not in context:
            context[var] = ""

    sig = signature(getattr(definer, "func", definer))
    depends_on = []
    if 'depends_on' in sig.parameters:
        depends_on_default = sig.parameters['depends_on'].default
        depends_on = context.get('depends_on', depends_on_default) or []

    if depends_on is None:
        depends_on = []
    if not isinstance(depends_on, (list, tuple, set)):
        raise TypeError("depends_on must be list, tuple, or set.")

    variables_needed_map = _get_variables_map(set(), definer)

    missing = []
    for var_name, trace in variables_needed_map.items():
        if var_name in context:
            continue

        if var_name in sig.parameters and sig.parameters[var_name].default is not inspect.Parameter.empty:
            continue

        is_dependency_name = False
        for dep in depends_on:
            dep_name = getattr(dep, '__name__', str(dep))
            if var_name == dep_name:
                is_dependency_name = True
                break
        if is_dependency_name:
            continue
        missing.append((var_name, trace))
    if not missing:
        return True
    messages = []
    for v, trace in missing:
        messages.append(f"'{v}' (found in: {' -> '.join(trace)})")

    message = (
        "The following Jinja variables are not defined in the context and do not have default values "
        "defined in the definer's signature:\n"
        + "\n".join(messages)
    )
    raise ValueError(message)

@conditional(extends=_COMPONENT, conditions=[_check_context])
class COMPONENT:
    pass

Content = Union(Markdown, Extension('md'))

@model(extends=COMPONENT)
class _STATIC:
    marker: Optional(Str, "content")
    content: Content
    frontmatter: Optional(Json, {})

@typed
def _check_static_context(static: _STATIC) -> Bool:
    definer = static.get('definer', _nill_definer())
    marker = static.get('marker', 'content')
    context = static.get('context', {})
    params = set(signature(definer).parameters)
    if marker in params:
        return False
    if marker in context:
        return False
    kwargs = {k: context[k] for k in params if k in context}
    try:
        jinja_str = definer(**kwargs)
    except Exception:
        return False
    pattern = r"\{\{\s*" + re.escape(marker) + r"\s*\}\}"
    found = re.search(pattern, jinja_str) is not None
    return found

@conditional(extends=_STATIC, conditions=[_check_static_context])
class STATIC:
    pass

@model(extends=COMPONENT)
class _PAGE:
    auto_style: Optional(Bool, False)
    static_dir: Optional(Path, "")

@model(extends=STATIC)
class _STATIC_PAGE:
    auto_style: Optional(Bool, False)
    static_dir: Optional(Path, "")

@typed
def _check_page_core(page: Union(_PAGE, _STATIC)) -> Bool:
    from app.service import render
    errors = []
    html = render(COMPONENT(page))
    html_match = re.search(r"<html[^>]*>(.*?)</html>", html, flags=re.IGNORECASE | re.DOTALL)
    head_match = re.search(r"<head[^>]*>(.*?)</head>", html, flags=re.IGNORECASE | re.DOTALL)
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html, flags=re.IGNORECASE | re.DOTALL)

    if not html_match:
        errors.append("Missing <html> block.")
    if not head_match:
        errors.append("Missing <head> block.")
    if not body_match:
        errors.append("Missing <body> block.")

    if errors:
        err_text = "\n".join(errors)
        raise AssertionError(f"[check_page] Rendered HTML does not contain required block(s):\n{err_text}\nActual HTML:\n{html[:500]}...")

    html_content = html_match.group(1)

    html_outer_match = re.search(r"<html[^>]*>(.*?)</html>", html, flags=re.IGNORECASE | re.DOTALL)
    head_outer_match = re.search(r"<head[^>]*>(.*?)</head>", html, flags=re.IGNORECASE | re.DOTALL)
    body_outer_match = re.search(r"<body[^>]*>(.*?</body>)", html, flags=re.IGNORECASE | re.DOTALL)

    if not (html_outer_match and head_outer_match and body_outer_match):
        errors.append("One or more essential blocks (html, head, body) could not be located for structural analysis.")
    else:
        html_start, html_end = html_outer_match.span()
        head_start, head_end = head_outer_match.span()
        body_start, body_end = body_outer_match.span()

        if not (html_start < head_start < html_end and head_end < html_end):
            errors.append("<head> block is not contained within <html> block.")
        if not (html_start < body_start < html_end and body_end < html_end):
            errors.append("<body> block is not contained within <html> block.")

        html_opening_tag = re.match(r"<html[^>]*>", html, re.IGNORECASE)
        if html_opening_tag:
            text_before_head = html[html_opening_tag.end():head_start]
            if re.search(r"<[^/!][^>]*>", text_before_head): # Any open tag
                errors.append("<head> block is not a direct child of <html> (other tags found between them).")

            text_between_head_body = html[head_end:body_start]
            if re.search(r"<[^/!][^>]*>", text_between_head_body): # Any open tag
                errors.append("<body> block is not a direct child of <html> (other tags found between <head> and <body>).")
        else:
            errors.append("Could not find <html> opening tag for direct child check.")

        if body_start < head_start < body_end:
            errors.append("<head> block is found inside <body> block.")
        if head_start < body_start < head_end:
            errors.append("<body> block is found inside <head> block.")

    if errors:
        err_text = "\n".join(errors)
        raise AssertionError(f"[check_page] HTML structure validation failed:\n{err_text}\nActual HTML:\n{html[:500]}...")
    return True

@typed
def _check_page(page: _PAGE) -> Bool:
    return _check_page_core(page) and not 'content' in page

@typed
def _check_static_page(page: _STATIC_PAGE) -> Bool:
    return _check_page_core(page) and 'content' in page

@conditional(extends=_PAGE, conditions=[_check_page])
class PAGE:
    pass

@conditional(extends=_STATIC_PAGE, conditions=[_check_static_page])
class STATIC_PAGE:
    pass

_nill_jinja  = """jinja"""

@typed
def _nill_definer(tag_name: Str="") -> DEFINER:
    if tag_name:
        from app.mods.factories.base import Tag
        def wrapper() -> Tag(tag_name):
            return _nill_jinja
    else:
        from app.mods.types.base import Jinja
        def wrapper() -> Jinja:
            return _nill_jinja
    return definer(wrapper)

@typed
def _nill_comp(tag_name: Str="") -> _COMPONENT:
    return {
        "definer": _nill_definer(tag_name),
        "context": {}
    }

@typed
def _nill_static() -> _STATIC:
    return {
        "definer": _nill_definer(),
        "context": {},
        "content": ""
    }
