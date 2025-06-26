```python
  /$$$$$$   /$$$$$$   /$$$$$$
 |____  $$ /$$__  $$ /$$__  $$
  /$$$$$$$| $$  \ $$| $$  \ $$
 /$$__  $$| $$  | $$| $$  | $$
|  $$$$$$$| $$$$$$$/| $$$$$$$/
 \_______/| $$____/ | $$____/
          | $$      | $$
          | $$      | $$
          |__/      |__/
```
# About

`app` is a Python framework to build web applications presenting type safety, from APIs to static pages.
 
# Overview

The lib is an extension of [fastapi](https://github.com/fastapi/fastapi), constructed using [pythonaltal/typed](https://github.com/pythonalta/typed) to ensure type safety. The lib includes a component system compatible with [jinja2](https://jinja.palletsprojects.com/en/stable/) and with [markdown](https://github.com/Python-Markdown/markdown) (for static components), and provides a lot of ready to use components in `app.components`.

# Install

With `pip`:
```bash
pip install git+https://github.com/pythonalta/  
```

With [py](https://github.com/ximenesyuri/py):
```bash
py i pythonalta/app  
```

# Components

In `app` component system, the unities are the `components`, which are objects of type `Component`. They are defined by two data:
1. `definer`: a typed function `f: Any -> JinjaStr` returning a `jinja string`, which is any string starting with `"""jinja` and containing [jinja2](https://jinja.palletsprojects.com/en/stable/) syntax;
2. `context`: a dictionary whose keys contains, at least, the definer variables.

A typical `definer` is as follows: 
```python
@typed
def my_definer(x: SomeType, y: OtherType, ...) -> JinjaStr:
    return """jinja
{{ for i in x }}
    <something>
        {{ if y is True }}
             <more html>
             ...
        {{ endif }}
    </something>
{{ endfor }}
"""
```

Notice that its variables are incorporated in the `jinja string`. Naturally, you could also manipulate these variables before passing them to the `jinja str`, e.g, by calling other external functions. The `jinja string` could also contains "free variables", which are not directly assigned by the `definer`:

```python
@typed
def my_definer(x: SomeType, y: OtherType, ...) -> JinjaStr:
    return """jinja
{{ for i in x }}
    <something>
        {{ if y is True }}
             <more html>
             ...
             {{ a_free_var }}
             ...
        {{ endif }}
    </something>
{{ endfor }}
"""
```

> See [jinja2](https://jinja.palletsprojects.com/en/stable/) to discover the full valid syntax.

The `context` of a component is a dictionary that provides values for all the variables in the `jinja string`:
1. the assigned by the `definer`
2. and those are "free variables". 

So, a context for the example above should be something as:

```python
my_context = {
    "x": some_value,
    "y": other_value,
    "a_free_var": another_value
}
```

The defined `component` is then given by:

```python
my_component = {
    "definer": my_definer,
    "context": my_context
}
```

If you then check `isinstance(my_component, Component)` this will return `True` if all the above conditions are satisfied. It will be `False` or will raise a `TypeError` depending on which condition is not satisfied.

### Rendering

One time constructed, components can be `rendered`: the process of evaluating the `context` of the `component` in the `jinja string` of the underlying `definer`, producing raw `html`.

The `render` process is implemented as a typed function `render: Component -> HTML`, available in `app.service`. It can be called directly, or as part of the construction of the return type of certain `endpoints`, as will be discussed later.

### Nested Components

Components can depend on other components, which is realized at the `definer` level. More precisely, a `definer` can be endowed with a special `depends_on` variable, which lists other already defined `definer`s. In this case, the dependent `definer`s can be called inside the `jinja string` of the main `definer`.

```python
@typed
def definer_1(...) -> JinjaStr:
    return """jinja
    ...
"""

@typed
def definer_2(...) -> JinjaStr:
    return """jinja
    ...
"""

@typed
def definer_3(..., depends_on=[definer_1, definer_2]) -> JinjaStr:
    return """jinja
    ...
{{ definer_1(...) }}
    ...
{{ definer_2(...) }}
"""
```

# Statics


```python
from app import App, Render
app = App()

@app.get("/...")
def endpoint_callback(some_var: SomeType ...) -> Render
    return Render(
        entity=some_page_model_entity,
        message="..."
    )

@app.post("/...")
def endpoint_callback(some_var: SomeType ...) -> Json
    return Json(
    )
```

```python
from app import Router
some_router = Router()

@some_router.get("/...")
def endpoint_callback(some_var: SomeType ...) -> Render
    return Render(
        entity=some_page_model_entity,
        message="..."
    )

app.include_router(some_router, prefix="...")

if __name__ == __main__:

app.run()
```

```python
from app import StaticApp

app = StaticApp(
    base_url="",
    dist_dir="",
    static_dir=""
)

@app.build("/path/to/somewhere")               # generates '/path/to/somewhere
def build_path_callback() -> Build
    return Build(
        entity=some_static_page_model_entity,
        content=some_content,
    )
```

```python
from app import Builder

some_builder = Builder()

@some_builder.build("/path/to/somewhere")               # generates '/path/to/somewhere
def build_path_callback() -> Build
    return Build(
        entity=some_static_page_model_entity,
        content=some_content
    )

app.include_builder("...", prefix="...", static_dir="...")

if __name__ == __main__:

app.run()
```
