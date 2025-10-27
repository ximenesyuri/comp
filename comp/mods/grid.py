import inspect
from utils import text, mod, func
from typed import typed, optional, null, Str, Typed, MODEL, Any, TYPE, name, Maybe
from typed.mods.helper.helper import _check_codomain
from comp.models.structure import Grid, Row, Col
from comp.comps.structure import grid
from comp.comps.responsive import desktop, tablet, phone
from comp.mods.operations import eval
from comp.mods.types.base import COMPONENT
from comp.mods.err import GridErr

@optional
class GridEntity:
    desktop: Any
    tablet: Any
    phone: Any

@optional
class GridFactory:
    desktop: Typed(Any, cod=Grid)
    tablet: Typed(Any, cod=Grid)
    phone: Typed(Any, cod=Grid)

@typed
def build_col(model: MODEL) -> Typed:
    model_name = model.__name__
    model_snake = text.camel_to_snake(model_name)
    frame_info = inspect.stack()[3]
    frame = frame_info.frame
    caller_globals = frame.f_globals

    print(model.__bases__)

    if len(model.__bases__) != 5:
        raise GridErr(
            f"Could not create a col factory for model '{model_name}':\n"
            f"  ==> '{model_name}': model extends an unexpected number of types.\n"
             "      [expected_number] 3+2\n"
            f"      [received_number] {len(model.__bases__)}"
        )

    if Col not in model.__bases__:
        raise GridErr(
            f"Could not create a col factory for model '{model_name}':\n"
            f"  ==> '{model_name}': model does not extends 'Col'."
        )

    base_model = [b for b in model.__bases__ if b is not Col]
    base_model = base_model[0]
    base_model_name = base_model.__name__

    attrs = {}
    col_attrs = tuple(Col.__dict__.get('optional_attrs', {}).keys())
    base_model_attrs = tuple(base_model.__dict__.get('optional_attrs', {}).keys())
    print(base_model)
    print(base_model_attrs)
    for k, v in model.__dict__.get('optional_attrs', {}).items():
        if k not in col_attrs:
            if k not in base_model_attrs:
                raise GridErr(
                    f"Could not create a col factory for model '{model_name}':\n"
                    f"  ==> '{model_name}': model has an unexpected attribute.\n"
                    f"      [received_attr] '{name(k)}'"
                )
            attrs.update({k: v['type']})
    for k, v in model.__dict__.get('mandatory_attrs', {}).items():
        if k not in col_attrs:
            if k not in base_model_attrs:
                raise GridErr(
                    f"Could not create a col factory for model '{model_name}':\n"
                    f"  ==> '{model_name}': model has an unexpected attribute.\n"
                    f"      [received_attr] '{name(k)}'"
                )
            attrs.update({k: v['type']})

    base_model_calls = [
        f"{field}={model_snake}.{field}" for field in attrs
    ]
    base_model_line = ',\n            '.join(base_model_calls)

    func_code = f"""
from typed import typed
from comp import Col, {base_model_name}

@typed
def {model_snake}({model_snake}: {model_name}={model_name}()) -> Col:
    return Col(
        col_id={model_snake}.col_id,
        col_class={model_snake}.col_class,
        col_style={model_snake}.col_style,
        col_inner={base_model_name}(
            {base_model_line}
        )
    )
"""
    local_ns = {}
    global_ns = caller_globals

    global_ns.update({
        'typed': typed,
        'Col': Col,
        model_name: model,
        base_model_name: base_model,
        'getattr': getattr,
    })
    exec(func_code, global_ns, local_ns)
    return local_ns[model_snake]

@typed
def build_row(model: MODEL, cols_module: Str = '') -> Typed:
    model_name = model.__name__
    model_snake = text.camel_to_snake(model_name)

    if Row not in model.__bases__:
        raise GridErr(
            f"Could not create a row factory for model '{model_name}':\n"
            f"  ==> '{model_name}': model does not extends 'Row'."
        )

    frame_info = inspect.stack()[3]
    frame = frame_info.frame
    caller_globals = frame.f_globals
    caller_module_name = caller_globals.get('__name__', None)
    attrs = {}
    row_attrs = tuple(Row.__dict__.get('optional_attrs', {}).keys())
    for k, v in model.__dict__.get('optional_attrs', {}).items():
        if k not in row_attrs:
            attrs.update({k: v['type']})
    for k, v in model.__dict__.get('mandatory_attrs', {}).items():
        if k not in row_attrs:
            attrs.update({k: v['type']})

    available_attr_names = []
    import_line = ''

    if cols_module:
        if mod.exists(cols_module):
            for attr_name in tuple(attrs.keys()):
                try:
                    obj = mod.get_global(cols_module, attr_name)
                except:
                    raise GridErr(
                        f"Could not create a row factory for model '{model_name}':\n"
                        f"  ==> '{attr_name}': object does not exist in module '{cols_module}'."
                    ) from None
                codomain = getattr(obj, 'codomain', None)
                if codomain is not Col:
                    raise GridErr(
                        f"Could not create a row factory for model '{model_name}':\n"
                        f"  ==> '{name(obj)}': is not a Col factory."
                    )
                domain = getattr(obj, 'domain', None)
                if len(domain) != 2:
                    raise GridErr(
                        f"Could not create a row factory for model '{name(model)}':\n"
                        f"  ==> '{name(attr_name)}': attribute has an unexpected number of arguments\n"
                         "      [expected_args]: 2\n"
                        f"      [received_args]: {len(domain)}"
                    )
                attr_param_name = func.params.name(func.unwrap(obj))[1]
                if attr_param_name != attr_name:
                    raise GridErr(
                        f"Could not create a row factory for model '{model_name}':\n"
                        f"  ==> '{name(attr_name)}': attribute has an unexpected parameter name\n"
                        f"      [expected_name]: {attr_name}\n"
                        f"      [received_name]: {attr_param_name}"
                    )
                attr_type = domain[1]
                if attr_type.__name__ != text.snake_to_camel(attr_name):
                    raise GridErr(
                        f"Could not create a row factory for model '{model_name}':\n"
                        f"  ==> '{name(attr_name)}': attribute has an unexpected type\n"
                        f"      [expected_type]: {text.snake_to_camel(attr_name)}\n"
                        f"      [received_type]: {attr_type.__name__}"
                    )
                try:
                    from typed import null
                    _check_codomain(obj, Col, codomain, obj(null(attr_type)))
                except:
                    raise GridErr(
                        f"Could not create a row factory for model '{model_name}':\n"
                        f"  ==> '{name(attr_name)}': is not returning an instance of Col"
                    )
                available_attr_names.append(attr_name)

            if available_attr_names:
                imports = ', '.join(available_attr_names)
                import_line = f"from {cols_module} import {imports}"
        else:
            raise GridErr(
                f"Could not create a row factory for model '{model_name}':\n"
                f"  ==> '{cols_module}': module does not exist."
            )
    else:
        for attr_name in tuple(attrs.keys()):
            try:
                obj = mod.get_global(caller_module_name, attr_name)
            except:
                raise GridErr(
                    f"Could not create a row factory for model '{model_name}':\n"
                    f"  ==> '{attr_name}': object does not exist in module '{caller_module_name}'."
                ) from None
            codomain= getattr(obj, 'codomain', None)
            if codomain is not Col:
                raise GridErr(
                    f"Could not create a row factory for model '{model_name}':\n"
                    f"  ==> '{name(obj)}': attribute is not a Col factory."
                )
            domain = getattr(obj, 'domain', None)
            if len(domain) != 2:
                raise GridErr(
                    f"Could not create a row factory for model '{model_name}':\n"
                    f"  ==> '{name(attr_name)}': attribute has an unexpected number of arguments\n"
                     "      [expected_args]: 2\n"
                    f"      [received_args]: {len(domain)}"
                )
            attr_param_name = func.params.name(func.unwrap(obj))[1]
            if attr_param_name != attr_name:
                raise GridErr(
                    f"Could not create a row factory for model '{model_name}':\n"
                    f"  ==> '{name(attr_name)}': attribute has an unexpected parameter name\n"
                    f"      [expected_name]: {attr_name}\n"
                    f"      [received_name]: {attr_param_name}"
                )
            attr_type = domain[1]
            if attr_type.__name__ != text.snake_to_camel(attr_name):
                raise GridErr(
                    f"Could not create a row factory for model '{model_name}':\n"
                    f"  ==> '{name(attr_name)}': attribute has an unexpected type\n"
                    f"      [expected_type]: {text.snake_to_camel(attr_name)}\n"
                    f"      [received_type]: {name(attr_type)}"
                )
            try:
                from typed import null
                _check_codomain(obj, Col, codomain, obj(null(attr_type)))
            except:
                raise GridErr(
                    f"Could not create a row factory for model '{model_name}':\n"
                    f"  ==> '{name(attr_name)}': is not returning an instance of Col"
                )
            available_attr_names.append(attr_name)

    col_calls = [
        f"{field}({model_snake}.{field})" for field in available_attr_names
    ]
    row_cols = ',\n            '.join(col_calls)

    func_code = f"""
from typed import typed
from comp import Row

{import_line}

@typed
def {model_snake}({model_snake}: {model_name}={model_name}()) -> Row:
    return Row(
        row_id={model_snake}.row_id,
        row_class={model_snake}.row_class,
        row_style={model_snake}.row_style,
        row_cols=[
            {row_cols}
        ]
    )
"""
    local_ns = {}
    global_ns = caller_globals.copy()

    global_ns.update({
        'typed': typed,
        'Row': Row,
        model_name: model,
        'getattr': getattr,
    })

    if cols_module and available_attr_names:
        mod_obj = mod.get(cols_module)
        for name in available_attr_names:
            global_ns[name] = getattr(mod_obj, name)

    exec(func_code, global_ns, local_ns)
    return local_ns[model_snake]

@typed
def build_grid(model: MODEL, rows_module: Str='') -> Typed:
    model_name = model.__name__
    model_snake = text.camel_to_snake(model_name)

    if Grid not in model.__bases__:
        raise GridErr(
            f"Could not create a grid factory for model '{model_name}':\n"
            f"  ==> '{model_name}': model does not extends 'Grid'."
        )

    frame_info = inspect.stack()[3]
    frame = frame_info.frame
    caller_globals = frame.f_globals
    caller_module_name = caller_globals.get('__name__', None)
    attrs = {}
    grid_attrs = tuple(Grid.__dict__.get('optional_attrs', {}).keys())
    for k, v in model.__dict__.get('optional_attrs', {}).items():
        if k not in grid_attrs:
            attrs.update({k: v['type']})
    for k, v in model.__dict__.get('mandatory_attrs', {}).items():
        if k not in grid_attrs:
            attrs.update({k: v['type']})

    available_attr_names = []
    import_line = ''

    if rows_module:
        if mod.exists(rows_module):
            for attr_name in tuple(attrs.keys()):
                try:
                    obj = mod.get_global(rows_module, attr_name)
                except:
                    raise GridErr(
                        f"Could not create a row factory for model '{model_name}':\n"
                        f"  ==> '{attr_name}': object does not exist in module '{caller_module_name}'."
                    ) from None
                codomain = getattr(obj, 'codomain', None)
                if codomain and codomain is not Row:
                    raise GridErr(
                        f"Could not create a grid factory for model '{model_name}':\n"
                        f"  ==> '{name(obj)}': is not a Row factory."
                    )
                domain = getattr(obj, 'domain', None)
                if domain and len(domain) != 2:
                    raise GridErr(
                        f"Could not create a row factory for model '{model_name}':\n"
                        f"  ==> '{name(attr_name)}': attribute has an unexpected number of arguments\n"
                         "      [expected_args]: 2\n"
                        f"      [received_args]: {len(domain)}"
                    )
                attr_param_name = func.params.name(func.unwrap(obj))[1]
                if attr_param_name != attr_name:
                    raise GridErr(
                        f"Could not create a grid factory for model '{model_name}':\n"
                        f"  ==> '{name(attr_name)}': attribute has an unexpected parameter name\n"
                        f"      [expected_name]: {attr_name}\n"
                        f"      [received_name]: {attr_param_name}"
                    )
                attr_type = domain[1]
                if attr_type.__name__ != text.snake_to_camel(attr_name):
                    raise GridErr(
                        f"Could not create a grid factory for model '{model_name}':\n"
                        f"  ==> '{name(attr_name)}': attribute has an unexpected type\n"
                        f"      [expected_type]: {text.snake_to_camel(attr_name)}\n"
                        f"      [received_type]: {name(attr_type)}"
                    )

                available_attr_names.append(attr_name)

            if available_attr_names:
                imports = ', '.join(available_attr_names)
                import_line = f"from {rows_module} import {imports}"
        else:
            raise GridErr(
                f"Could not create a grid factory for model '{model_name}':\n"
                f"  ==> '{rows_module}': module does not exist."
            )
    else:
        for attr_name in tuple(attrs.keys()):
            try:
                obj = mod.get_global(caller_module_name, attr_name)
            except:
                raise GridErr(
                    f"Could not create a row factory for model '{model_name}':\n"
                    f"  ==> '{attr_name}': object does not exist in module '{caller_module_name}'."
                ) from None
            codomain= getattr(obj, 'codomain', None)
            if codomain and codomain is not Row:
                raise GridErr(
                    f"Could not create a grid factory for model '{model_name}':\n"
                    f"  ==> '{name(obj)}': attribute is not a Row factory."
                )
            domain = getattr(obj, 'domain', None)
            if domain and len(domain) != 2:
                raise GridErr(
                    f"Could not create a grid factory for model '{model_name}':\n"
                    f"  ==> '{name(attr_name)}': attribute has an unexpected number of arguments\n"
                     "      [expected_args]: 2\n"
                    f"      [received_args]: {len(domain)}"
                )
            attr_param_name = func.params.name(func.unwrap(obj))[1]
            if attr_param_name != attr_name:
                raise GridErr(
                    f"Could not create a grid factory for model '{model_name}':\n"
                    f"  ==> '{name(attr_name)}': attribute has an unexpected parameter name\n"
                    f"      [expected_name]: {attr_name}\n"
                    f"      [received_name]: {attr_param_name}"
                )
            attr_type = domain[1]
            if attr_type.__name__ != text.snake_to_camel(attr_name):
                raise GridErr(
                    f"Could not create a grid factory for model '{model_name}':\n"
                    f"  ==> '{name(attr_name)}': attribute has an unexpected type\n"
                    f"      [expected_type]: {text.snake_to_camel(attr_name)}\n"
                    f"      [received_type]: {name(attr_type)}"
                )
            available_attr_names.append(attr_name)

    row_calls = [
        f"{field}({model_snake}.{field})" for field in available_attr_names
    ]
    grid_rows = ',\n            '.join(row_calls)

    func_code = f"""
from typed import typed
from comp import Grid
{import_line}

@typed
def {model_snake}({model_snake}: {model_name}={model_name}()) -> Grid:
    return Grid(
        grid_id={model_snake}.grid_id,
        grid_class={model_snake}.grid_class,
        grid_style={model_snake}.grid_style,
        grid_rows=[
            {grid_rows}
        ]
    )
"""
    local_ns = {}
    global_ns = caller_globals.copy()

    global_ns.update({
        'typed': typed,
        'Grid': Grid,
        model_name: model,
        'getattr': getattr,
    })
    exec(func_code, global_ns, local_ns)
    return local_ns[model_snake]

@typed
def build_factory(model: MODEL, grids_module: Str='') -> GridFactory:
    frame_info = inspect.stack()[3]
    frame = frame_info.frame
    caller_globals = frame.f_globals
    caller_module_name = caller_globals.get('__name__', None)
    model_name = model.__name__
    model_snake = text.camel_to_snake(model_name)
    responsive_attrs = ('desktop', 'tablet', 'phone')
    attrs = {}
    for k, v in model.__dict__.get('optional_attrs', {}).items():
        if k.split('_')[0] in responsive_attrs:
            attrs.update({k: v['type']})
    for k, v in model.__dict__.get('mandatory_attrs', {}).items():
        if k.split('_')[0] in responsive_attrs:
            attrs.update({k: v['type']})

    available_attr_names = []
    import_line = ''

    if grids_module:
        if mod.exists(grids_module):
            for attr_name in tuple(attrs.keys()):
                try:
                    obj = mod.get_global(grids_module, attr_name)
                except:
                    raise GridErr(
                        f"Could not create a row factory for model '{model_name}':\n"
                        f"  ==> '{attr_name}': object does not exist in module '{grids_module}'."
                    ) from None
                codomain = getattr(obj, 'codomain', None)
                if codomain and codomain is not Grid:
                    raise GridErr(
                        f"Could not instantiate GridFactory for model '{model_name}':\n"
                        f"  ==> '{name(obj)}': is not a grid factory."
                    )
                domain = getattr(obj, 'domain', None)
                if domain and len(domain) != 2:
                    raise GridErr(
                        f"Could not instantiate GridFactory for model '{model_name}':\n"
                        f"  ==> '{name(attr_name)}': attribute has an unexpected number of arguments\n"
                         "      [expected_args]: 2\n"
                        f"      [received_args]: {len(domain)}"
                    )
                attr_param_name = func.params.name(func.unwrap(obj))[1]
                if attr_param_name != attr_name:
                    raise GridErr(
                        f"Could not instantiate GridFactory for model '{model_name}':\n"
                        f"  ==> '{name(attr_name)}': attribute has an unexpected parameter name\n"
                        f"      [expected_name]: {attr_name}\n"
                        f"      [received_name]: {attr_param_name}"
                    )
                attr_type = domain[1]
                if attr_type.__name__ != getattr(model, attr_name).__name__:
                    raise GridErr(
                        f"Could not instantiate GridFactory for model '{model_name}':\n"
                        f"  ==> '{name(attr_name)}': attribute has an unexpected type\n"
                        f"      [expected_type]: {text.snake_to_camel(attr_name)}\n"
                        f"      [received_type]: {attr_type.__name__}"
                    )
                try:
                    from typed import null
                    _check_codomain(obj, Grid, codomain, obj(null(attr_type)))
                except:
                    raise GridErr(
                        f"Could not instantiate GridFactory for model '{model_name}':\n"
                        f"  ==> '{name(attr_name)}': is not returning an instance of Grid."
                    )

                available_attr_names.append(attr_name)

            if available_attr_names:
                imports = ', '.join(available_attr_names)
                import_line = f"from {grids_module} import {imports}"
        else:
            raise GridErr(
                f"Could not instantiate GridFactory for model '{model_name}':\n"
                f"  ==> '{grids_module}': module does not exist."
            )
    else:
        for attr_name in tuple(attrs.keys()):
            try:
                obj = mod.get_global(caller_module_name, attr_name)
            except:
                raise GridErr(
                    f"Could not create a row factory for model '{model_name}':\n"
                    f"  ==> '{attr_name}': object does not exist in module '{caller_module_name}'."
                ) from None
            codomain= getattr(obj, 'codomain', None)
            if codomain and codomain is not Grid:
                raise GridErr(
                    f"Could not instantiate GridFactory for model '{model_name}':\n"
                    f"  ==> '{name(obj)}': attribute is not a grid factory."
                )
            domain = getattr(obj, 'domain', None)
            if domain and len(domain) != 2:
                raise GridErr(
                    f"Could not instantiate GridFactory for model '{model_name}':\n"
                    f"  ==> '{name(attr_name)}': attribute has an unexpected number of arguments\n"
                     "      [expected_args]: 2\n"
                    f"      [received_args]: {len(domain)}"
                )
            attr_param_name = func.params.name(func.unwrap(obj))[1]
            if attr_param_name != attr_name:
                raise GridErr(
                    f"Could not instantiate GridFactory for model '{model_name}':\n"
                    f"  ==> '{name(attr_name)}': attribute has an unexpected parameter name\n"
                    f"      [expected_name]: {attr_name}\n"
                    f"      [received_name]: {attr_param_name}"
                )
            attr_type = domain[1]
            if not attr_type is getattr(model, attr_name) and not Maybe(attr_type) is getattr(model, attr_name):
                raise GridErr(
                    f"Could not instantiate GridFactory for model '{model_name}':\n"
                    f"  ==> '{name(attr_name)}': attribute has an unexpected type\n"
                    f"      [expected_type]: {text.snake_to_camel(attr_name)}\n"
                    f"      [received_type]: {attr_type.__name__}"
                )
            available_attr_names.append(attr_name)

    attr_code_line = ", ".join([f"{attr.split('_')[0]}={attr}" for attr in tuple(attrs.keys())])

    func_code = f"""
from comp import GridFactory

{import_line}
{model_snake} = GridFactory({attr_code_line})
"""
    local_ns = {}
    global_ns = caller_globals.copy()

    global_ns.update({
        'typed': typed,
        'Grid': Grid,
        model_name: model,
        'getattr': getattr,
    })
    exec(func_code, global_ns, local_ns)
    return local_ns[model_snake]

@typed
def build_comp(grid_entity: GridEntity, grid_factory: GridFactory) -> COMPONENT:
    if grid_entity.desktop:
        if not grid_factory.desktop:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_factory)}': missing 'desktop' grid factory"
            )
        if not len(grid_factory.desktop.domain) == 2:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_factory.desktop)}': has unexpected number of arguments\n"
                 '     [expected_arguments] 2\n'
                f"     [received_arguments] {len(grid_factory.desktop.domain)}"
            )
        if not grid_entity.desktop in grid_factory.desktop.domain[1]:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_entity.desktop)}': has unexpected type\n"
                f'     [expected type] subtype of {TYPE(grid_factory.desktop.domain[1])}\n'
                f"     [received_type] {name(TYPE(grid_entity.desktop))}"
            )
        desktop_grid = desktop * eval(grid, grid=grid_factory.desktop(grid_entity.desktop))
    else:
        desktop_grid = null(COMPONENT)
    if grid_entity.tablet:
        if not grid_entity.tablet:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_factory)}': missing 'tablet' grid factory"
            )
        if not len(grid_factory.tablet.domain) == 2:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_factory.tablet)}': has unexpected number of arguments\n"
                 '     [expected_arguments] 2\n'
                f"     [received_arguments] {len(grid_factory.tablet.domain)}"
            )
        if not grid_entity.tablet in grid_factory.tablet.domain[1]:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_entity.tablet)}': has unexpected type\n"
                f'     [expected_type] subtype of {TYPE(grid_factory.tablet.domain[1])}\n'
                f"     [received_type] {name(TYPE(grid_entity.tablet))}"
            )
        tablet_grid = tablet * eval(grid, grid=grid_factory.tablet(grid_entity.tablet))
    else:
        tablet_grid = null(COMPONENT)
    if grid_entity.phone:
        if not grid_factory.phone:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_factory)}': missing 'phone' grid factory"
            )
        if not len(grid_factory.phone.domain) == 2:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_factory.phone)}': has unexpected number of arguments\n"
                 '     [expected_arguments] 2\n'
                f"     [received_arguments] {len(grid_factory.phone.domain)}"
            )
        if not grid_entity.phone in grid_factory.phone.domain[1]:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_entity.phone)}': has unexpected type\n"
                f'     [expected type] subtype of {TYPE(grid_factory.phone.domain[1])}\n'
                f"     [received_type] {name(TYPE(grid_entity.phone))}"
            )
        phone_grid = phone * eval(grid, grid=grid_factory.phone(grid_entity.phone))
    else:
        phone_grid = null(COMPONENT)
    return desktop_grid + tablet_grid + phone_grid
