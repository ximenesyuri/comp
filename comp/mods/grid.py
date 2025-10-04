from typed import typed, optional, null, Typed, Any, TYPE, name
from comp.models.structure import Grid
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
def build_grid(grid_entity: GridEntity, grid_factory: GridFactory) -> COMPONENT:
    if grid_entity.desktop:
        if not grid_factory.desktop:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_factory)}': missing 'desktop' grid factory"
            )
        if not len(grid_factory.desktop.domain) == 1:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_factory.desktop)}': has unexpected number of arguments\n"
                 '     [expected_arguments] 1\n'
                f"     [received_arguments] {len(grid_factory.desktop.domain)}"
            )
        if not grid_entity.desktop in grid_factory.desktop.domain[0]:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_entity.desktop)}': has unexpected type\n"
                f'     [expected type] subtype of {TYPE(grid_factory.desktop.domain[0])}\n'
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
        if not len(grid_factory.tablet.domain) == 1:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_factory.tablet)}': has unexpected number of arguments\n"
                 '     [expected_arguments] 1\n'
                f"     [received_arguments] {len(grid_factory.tablet.domain)}"
            )
        if not grid_entity.tablet in grid_factory.tablet.domain[0]:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_entity.tablet)}': has unexpected type\n"
                f'     [expected_type] subtype of {TYPE(grid_factory.tablet.domain[0])}\n'
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
        if not len(grid_factory.phone.domain) == 1:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_factory.phone)}': has unexpected number of arguments\n"
                 '     [expected_arguments] 1\n'
                f"     [received_arguments] {len(grid_factory.phone.domain)}"
            )
        if not grid_entity.phone in grid_factory.phone.domain[0]:
            raise GridErr(
                "Could no build the responsive grid.\n"
                f" ==> '{name(grid_entity.phone)}': has unexpected type\n"
                f'     [expected type] subtype of {TYPE(grid_factory.phone.domain[0])}\n'
                f"     [received_type] {name(TYPE(grid_entity.phone))}"
            )
        phone_grid = phone * eval(grid, grid=grid_factory.phone(grid_entity.phone))
    else:
        phone_grid = null(COMPONENT)
    return desktop_grid + tablet_grid + phone_grid
