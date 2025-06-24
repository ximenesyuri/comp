```python
from typed.models import Model, Instance
from app import JinjaStr

StaticComponent = JinjaStr

PreComponent=Model(
    definer=Definer,
    depends_on=Optional(List(Definer), [])
)

ComponentCore = Model(
    precomponent=PreComponent,
    context=Json
)

Component = Filter(ComponentCore, "context contains definer arguments")

CONSTRUCTION: every definer defines a component

@typed
def component_definer(var_1: SomeType) -> JinjaStr:
    return """jinja
        ...
    """

@component
def component_definer(var_1: SomeType) -> JinjaStr:
    return """jinja
        ...
    """

component = Instance(
    model=Component,
    instance={
        "definer": component_definer_1,
        "context": ...,
        "depends_on": [component_2, component_3]
    }  
)

PageStructure = Model(
    metadata=Metadata,
    header=Header,
    footer=Footer,
    left_sidebar=Optional(LeftSidebar, jinill),
    right_sidebar=Optional(RightSidebar, jinill),
)

Page = Model(
    structure=PageStructure,
    context=Optional(Json, {})
    definer=Definer
)

StaticPage = Model(
    structure=PageStructure,
    context=Optional(Json, {})
    definer=StaticDefiner
)
```


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
