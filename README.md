```python
  /000000   /000000   /000000
 |____  00 /00__  00 /00__  00
  /0000000| 00  \ 00| 00  \ 00
 /00__  00| 00  | 00| 00  | 00
|  0000000| 0000000/| 0000000/
 \_______/| 00____/ | 00____/
          | 00      | 00
          | 00      | 00
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

# Component System

In the following we will briefly describe how the `app` component system works.

## Components

In `app` component system, the unities are the `components`, which are objects of type `Component`. They are defined by two data:
1. `definer`: a typed function `f: Any -> Jinja`, definer with the `@definer` decorator, and returning a `jinja string`: a string starting with `"""jinja` and containing [jinja2](https://jinja.palletsprojects.com/en/stable/) syntax;
2. `context`: a dictionary whose keys contains, at least, the definer variables.
           
A typical `definer` is as follows: 
```python
from typed import SomeType, OtherType
from app import definer, Jinja

@definer
def my_definer(x: SomeType, y: OtherType, ...) -> Jinja:
    return """jinja
{% for i in x %}
    <something>
        {% if y is True %}
             <more html>
                ...
             </more html>
        {% endif %}
    </something>  
{% endfor %}
"""
```
 
> 1. A `definer` is a "typed function" is the sense of [typed](https://github.com/pythonalta/typed). This means that all its arguments must have type hints (i.e type annotations), which are automatically verified at runtime. 
> 2. Notice that the variables of a `definer` are incorporated in the `jinja string`. Naturally, you could also manipulate these variables before passing them to the `jinja str`, e.g, by calling other external functions inside the body of the function defining the `definer`.
> 3. The `jinja string` could also contains "free variables", which are not directly assigned by the `definer`, as below.
> 4. See [jinja2](https://jinja.palletsprojects.com/en/stable/) to discover the full valid syntax for `jinja strings`. 

```python
from typed import typed, SomeType, OtherType
from app import Jinja

@typed
def my_definer(x: SomeType, y: OtherType, ...) -> Jinja:
    return """jinja
{% for i in x %}
    <something>
        {% if y is True %}
             <more html>
                ...
                {{ a_free_var }}
                ...
             </more html>
        {% endif %}
    </something>
{% endfor %}
"""
```

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

> There is also a `Context` factory, which can be used to define a context is a type safety way, using both `Json` or `kwargs` approaches, as below.
```python
from app import Context
...
my_context = Context({
    "x": some_value,
    "y": other_value,
    "a_free_var": another_value
})
...
my_context = Context(
    x=some_value,
    y=other_value,
    a_free_var=another_value
)
```

The corresponding `component` from the `definer` and `context` above is then given by:

```python
my_component = {
    "definer": my_definer,
    "context": my_context
}
```

If you then check `isinstance(my_component, Component)` this will return `True` if all the above conditions are satisfied. It will be `False` or will raise a `TypeError` depending on which condition is not satisfied.
 
> The type safe way to define a component is using the `Instance` checker from `typed.models`, or passing it directly as an argument to the `Component` type factory (using `Json` or `kwargs` approach):

```python
from typed.models import Instance
from app import Component
...
my_component = Instance(
    model=Component,
    entity={
        "definer": my_definer,
        "context": my_context
    }
)
...
my_component = Component({
    "definer": my_definer,
    "context": my_context
})
...
my_component = Component(
    definer=my_definer,
    context=my_context
)
```

## Tags

Typically, `components` are delimited by a HTML tag. In `app` one can create custom subtypes of `Component` associated with a HTML tag through the factory `Tag`. More precisely, an entity of `Tag('tag_name')` is a component whose `definer` is of type `TagDefiner('tag_name')`. In turn, a `definer` is an instance of `TagDefiner('tag_name')` precisely if its `codomain` is an instance of `TagStr('tag_name')`, which means that it returns a `jinja string` that is enclosed with the tag `<tag_name>`.

So, for example, an instance of `Tag(h1)` is any `component`

```python
my_component = {
    "definer": my_definer,
    "context": my_context
}
```

such that `my_definer` is defined as follows:

```python
from typed import SomeType, OtherType
from app import definer, TagStr

@definer
def my_definer(x: SomeType, y: OtherType, ...) -> TagStr('h1'):
    return """jinja
<h1 class="...">
    ...
</h1>
"""
```

There are certain predefined tag subtypes of `Component`, as follows:
```
subtype    definition     string type   definer type
------------------------------------------------------------- 
Html       Tag('html')    HtmlStr       HtmlDefiner
Head       Tag('head')    HeadStr       HeadDefiner 
Body       Tag('body')    BodyStr       BodyDefiner 
Header     Tag('header')  HeaderStr     HeaderDefiner 
Footer     Tag('footer')  FooterStr     FooterDefiner
Aside      Tag('aside')   AsideStr      AsideDefiner
...
```

## Rendering

One time constructed, components can be `rendered`: which is the process of evaluating the `context` of the `component` in the `jinja string` of its underlying `definer`, producing raw `html`.

The `render` process is implemented as a typed function `render: Component -> HTML`, available in `app.service`. It can be called directly, as below, or as part of the construction of the return type of certain `endpoints`, as will be discussed later.

```python
from app.service import Component, render
...
my_component = Component(
    definer=my_definer,
    context=my_context
)

html = render(my_component)
```

## Nested Components

Components can depend on other components. This is realized at the `definer` level. More precisely, a `definer` can be endowed with a special `depends_on` variable, which lists other already defined `definer`s. In this case, the dependent `definer`s can be called inside the `jinja string` of the main `definer`.

```python
from app import Jinja, TagStr, definer

@definer
def definer_1(...) -> Jinja:
    return """jinja
    ...
"""

@definer
def definer_2(...) -> TagStr('tag_name'):
    return """jinja
    ...
"""

@definer
def definer_3(..., depends_on=[definer_1, definer_2]) -> Jinja:
    return """jinja
    ...
{{ definer_1(...) }}
    ...
{{ definer_2(...) }}
"""
```

> Recall that `definer`s are "typed functions", which means that all their arguments must have type hints, which are checked at runtime. There is an exception: the `depends_on` variable. Indeed, if a type hint is not provided, then `List(Definer)` is automatically attached to it. On the other hand, if a type hint is provided, it must be a subtype of `List(Definer)`.
  
## Assets

While defining a `component`, it should be needed to include assets. 

## Statics

## Pages

In `app` component system, a very special kind of `component` is a `page`. It is such that its rendered HTML satisfies the following:
1. its most external HTML tag is `<html>`;
2. the `<html>` block contains blocks `<head>` and `<body>`;
3. `<head>` is not inside `<block>` and vice-versa.

Thus, in sum, a `page` is a `component` that, **after being rendered**, produces an HTML in the following format:

```html
...
<html>
    ...
    <head> ... </head>
    <body> ... </body>
    ...
</html>
...
```

There is the type `Page` of all `page`s. It is actually an extension of `Component` to include two entries:
1. `assets_dir`: a directory or a list of directories from which assets are collected
2. `auto_style`: if `<style>` block will be automatically generated or not

> In the same way as `Page` is an extension of `Component`, we have `StaticPage`, which is an extension of `Static`.

## Style

# App System

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
