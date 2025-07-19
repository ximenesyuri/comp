# About

In the following we will briefly describe how the `app` component system works.

<!-- toc -->

- [Components](#components)
- [Tags](#tags)
- [Dependences](#dependences)
- [Inners](#inners)
- [Operations](#operations)
- [Arithmetic](#arithmetic)
- [Models](#models)
- [Builtins](#builtins)
- [Rendering](#rendering)
- [Scripts and Assets](#scripts-and-assets)
- [Statics](#statics)
- [Pages](#pages)
- [Style](#style)

<!-- tocstop -->

# Components

In `app` component system, the basic unities are the _components_. A _component_ is a typed function (is the sense of [typed](https://github.com/ximenesyuri/typed)) taking values in the `Jinja` type, and being decorated with the `@component` decorator.

Thus, a typical component is defined as follows:
```python
from typed import SomeType, OtherType
from app import component, Jinja

@component
def my_comp(x: SomeType, y: OtherType, ...) -> Jinja:
    ...
    return """jinja
{% for i in x %}
<some html>
    {% if y is True %}
    <more html>
    ...
    </more html>
    {% endif %}
</some html>
{% endfor %}
"""
```

The type `Jinja` is the subtype of `Str` consisting of all strings which begins with the `jinja` keyword and that can be compiled in [jinja2](https://jinja.palletsprojects.com/en/stable/).
    
> 1. See [jinja2](https://jinja.palletsprojects.com/en/stable/) to discover the full valid syntax for `jinja strings`.
> 2. Local variables of a component are automatically included in the context of its returning `jinja string`. This means that you can define variables in the body of a component and then use the defined variables in the returning `jinja string`.

Each component comes equipped with the `jinja` property, which returns its raw `jinja string`:

```python
print(my_comp.jinja)

# will return the following:
# {% for i in x %}
# <some html>
#     {% if y is True %}
#     <more html>
#     ...
#     </more html>
#     {% endif %}
# </some html>
# {% endfor %}
```
  
# Tags
      
Typically, components are delimited by a HTML tag. In `app` there is a type factory `Tag: Tuple(Str) -> SUB(Jinja)` that receives a tuple of HTML tag names and returns the subtype of `Jinja` of all `jinja strings` enclosed by one of the given tags.

```python
# example of instance of 'Tag('some-tag')'
"""jinja
<some-tag>
...
</some-tag>
"""
```

With such type factory one can construct type safe tag-based components:

```python
from app import component, Tag

@component
def my_tag_comp(...) -> Tag('some-tag'):
    ...
    return """jinja
<some-tag>
...
</some-tag>
"""
```

There is a supplementary type factory `TAG: Tuple(Str) -> SUB(COMPONENT)` that associates to each tuple `(tag1, tag2, ...)` of HTML tags the corresponding subtype of `TAG(tag1, tag2, ...)` of `COMPONENT` of all components that return `Tag(tag1, tag2, ...)` strings.

```python
from app import TAG

# the following returns True
print(isinstance(my_tag_comp, TAG('some-tag')))
```

# Dependences
  
Components can depend on other components. More precisely, a component can be endowed with a special `__depends_on__` variable of type `List(COMPONENT)`, which lists other already defined components. In this case, the dependent components can be called inside the `jinja string` of the main component.

```python
from app import Jinja, Tag, component

@component
def comp_1(...) -> Jinja:
    ...
    return """jinja
    ...
"""

@component
def comp_2(...) -> Tag('some-tag'):
    ...
    return """jinja
<some-tag>
    ...
</some-tag>
"""

@component
def main_comp(..., __depends_on__=[comp_1, comp_2]) -> Jinja:
    ...
    return """jinja
    ...
{{ comp_1(...) }}
    ...
{{ comp_2(...) }}
"""
```

Recall that components are "typed functions", which means that all their arguments must have type hints, which are checked at runtime. There is an exception: the `__depends_on__` variable. Indeed, if a type hint is not provided, then `List(COMPONENT)` is automatically attached to it. On the other hand, if a type hint is provided, it must be a subtype of `List(COMPONENT)`.
   
# Inners
    
In `app`, components may have a special kind of variable: the `inner` variables, which are necessarily of type `Inner` and works as placeholders for future insert inside the component.

```python
from app import component, Tag, Inner

@component
def my_inner_comp(..., inner: Inner, ...) -> Tag('some-tag'):
    ...
    return """jinja
<some-tag>
    {{ inner }}
</some-tag>
"""
```

The `inner` variables of a given component can be collected from the property `inner_vars` in `COMPONENT`:

```python
print(my_inner_comp.inner_vars) # will return '1'
```

The number of `inner` vars is used to decompose the type `COMPONENT` into distinct subtypes of components with a fixed amount of `inner` variables. More precisely, there is the type factory `Component: Int -> SUB(COMPONENT)` that to each integer `n>=0` returns the subtype `Component(n)` of `COMPONENT` of all components such that `component.inner_vars == n`.

So, for example:

```python
from app import Component

print(isinstance(my_inner_comp, Component(1)) # will return 'True'
print(isinstance(my_inner_comp, Component(0)) # will return 'False' 
```

By definition, if `n<0`, then `Component(n)` is `COMPONENT`, meaning that the component may have any number of `inner` variables, including zero.

# Operations

There are three main operations involving components:
1. `join: COMPONENT x COMPONENT -> COMPONENT`:
    - receive a tuple of components and creates a new `component` whose `jinja string` is the join of the `jinja string`s of each provided `component`;
2. `concat: Component(1) x COMPONENT -> COMPONENT`:
    - receive a component with a single `inner` var and component, producing a new component whose `jinja str` is obtained by replacing the placeholder given by `inner` var in the first component with the `jinja string` of the second component.
3. `eval: COMPONENT x Dict(Any) -> COMPONENT`:
    - receive a component and a list of `key-value` and returns the component obtained by fixing each variable associated to a `key` with the corresponding `value`, leaving the other variables unchanged.

The intuition for each of such operations is as follows:
1. `join`: put a component **after** other component
2. `concat`: put a component **inside** other component
3. `eval`: from a component, **fixes** some part

So, for example, consider the following generic components:

```python
from typed import SomeType, OtherType
from app import Jinja, component, Tag, Inner, join, concat, eval

@component
def some_comp(x: SomeType, ...) -> Jinja
    ...
    return """jinja
{{ contents of 'comp_1' jinja var }}
"""

@component
def inner_comp(a: OtherType, inner: Inner, ...) -> Tag('some-tag')
    ...
    return """jinja
<some-tag>
    {{ inner }}
</some-tag>
"""
```

The resulting joined component `join(some_comp, inner_comp)` is equivalent to the following component:

```python
@component
def joined_comp(x: SomeType, ..., a: OtherType, inner: Inner, ...) -> Jinja:
    return """jinja
{{ contents of 'comp_1' jinja var }}
<some-tag>
    {{ inner }}
</some-tag>
"""
```

On the other hand, `concat(inner_comp, some_comp)` is equivalent to:

```python
@component
def concat_comp(a: OtherType, x: SomeType, ...) -> Tag('some-tag'):
    return """jinja
<some-tag>
    {{ contents of 'comp_1' jinja var }}
</some-tag>
"""
```

Finally, `eval(inner_comp, inner="blablabla")` is the same as defining the component below.

```python
@component
def eval_comp(a: OtherType, ...) -> Tag('some-tag'):
    return """jinja
<some-tag>
    blablabla
</some-tag>
"""
```

> In both `join` and `concat` operations, the `__depends_on__` is the concatenation of the `__depends_on__` of the underlying components. In the `eval` operation, on the other hand, the `__depends_on__` is maintained the same.

# Arithmetic

In the type `COMPONENT`, the operations `join` and `concat` corresponds, respectively to implementations of the class functions `__sum__` and `__mul__`. This means that instead of writing `join(comp_1, comp_2)` you can just write `comp_1 + comp_2`. Similarly, instead of `concat(comp_1, comp_2)`, you can write `comp_1 * comp_2`.

Therefore, the `COMPONENT` type  define a "component arithmetic" that can be used to build complex components from smaller ones.

# Models
 
Of course, a component accept tuples of variables of any type. However, a better way to organize the component is to assigns a `model` (in the sense of [typed](https://github.com/ximenesyuri/typed)) to it, grouping the variables in a more semantic entity.
    
```python
from typed import null, SomeType, OtherType, ...
from typed.models import model, Optional

@model
class MyComp:
    some_var: SomeType
    other_var: Optional(OtherType, null(OtherType))
    ...
```

Then, one can define a component as:

```python
from app import component, Jinja
from somewhere import MyComp

@component
def my_comp(my_comp: MyComp, ...) -> Jinja:
    return """jinja
    ...
    {{ my_comp.some_var }}
    ...
"""
```

# Builtins

Inside `app.models` you will encounter a plethora of ready to use models, one for each basic HTML tag, while in `app.components` you will find their corresponding components.

```
model       component       tag
---------------------------------------------------
Div         div             <div>
Text        text            <p>
Title       title           <h1>, <h2>, ... <h6>
Link        link            <a>
Image       image           <img>
Figure      figure          <figure>
Button      button          <button>
Script      script          <script>
Asset       asset           <link>
...
```

The builtin models have as attributes the main attributes of the corresponding HTML tag. So, for example:

```
model         attributes
----------------------------------
Div           div_id
              div_class
              ...
----------------------------------
Title         title_id
              title_class
              ...
----------------------------------
Image         img_id
              img_class
              img_href
              img_alt
              ...
```

From the builtin components and the `join` and `concat` operations you can build derived components very quickly. For instance, suppose you want to build a `div` with title followed by a paragraph. You can just take:

```python
from app.components import div, title, text

my_comp = div * (title + text)
```

The obtained component have the variables `div: Div`, `title: Title` and `text: Text`, whose attributes can then be fixed to produce concrete instances of `my_comp`.

# Rendering

One time constructed, components can be `rendered`: which is the process of evaluating the `component` in a `context`, producing raw HTML. More precisely, the `render` process is implemented as a typed function `render: Component x Context -> HTML`. 

```python
from app import render

html = render(my_comp, <context_vars>)
```

In practical terms, rendering a component is similarly to using `eval` operation applied to all variables of a component, followed by a `jinja` renderization. This means that if `some_var` is a variable of some component `my_comp`, then to render `my_comp` we need to pass `some_var` with some value:

```python
from typed import SomeType
from app import component, Jinja, render

@component
def my_comp(some_var: SomeType, ...) -> Jinja:
    ...
    return """jinja
    ....
"""

html = render(my_comp, some_var=some_value, ...)
```

> We note that, if in the definition of `my_comp` the variable `some_var` has a default value, it is used in `render` if the variable is omitted.
 
# Minify 

The `render` function has certain special variables, as we pass to discuss. The first of those variables in `__minify__`. It is a boolean variable with default value to `False`. If set to `True`, the obtained HTML is returned compacted.

So, if you want to produce compacted HTML, just use:

```python
from app import render

html = render(my_comp, <context_vars>, __minify__=True)
```

# Scripts

In the sequence, we have the variable `__scripts__` of type `List(Script)`. It should be used to append a component with certain auxiliary scripts. The `Script` model has a mandatory attribute `script_src` which defines its origin.

The attribute `script_src` is of type `Union(Extension('js'), Url('http', 'https')`, which means that it accepts both:
1. a `http` or `https` url
2. a path to some `.js` file.

If in `__script__` it is passed a script object with `script_src` given by a url, then, during the rendering, the component is appended with the builtin `script` component applied the given script object. On the other hand, if the script object contains a `script_src` which is the path to a `.js` file, then the content of the file is added to the component inside a `<script>` block.

So, for example, suppose you need to incorporate a script located in the url `https://my_script_url.com` to a component `my_comp`. All you need to do is:

```python
from app import render
from app.models import Script

my_script = Script(
    script_src="https://my_script_url.com",
    script_defer=True,
    ...
)

html = render(my_comp, <context_vars>, __scripts__=[my_script])
```

# Assets

# Extensions

# Style

# Statics

# Pages

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

