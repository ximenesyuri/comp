```python
from app import component, JinjaStr

Component = Model(
    definer=Definer,
    context=Optional(Json, {}),
    depends_on=Optional(List(Definer), [])
)

@typed
def component_definer(var_1: SomeType) -> JinjaStr:
    return """jinja
        ...
    """

component = Instance(
    model=ComponentModel,
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
from app import App
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
