import functools

import pytest

from modules.items.actions import To
from modules.items.inventory import InventoryMap, OutOfBoundsError
from modules.items.repository import TemplateRepository
from modules.items.types import Location


@pytest.fixture
def inventory_map(template_repository: TemplateRepository):
    return InventoryMap(template_repository=template_repository)


@pytest.mark.parametrize(
    "x,y,raises_error",
    [
        (-1, 0, True),
        (0, -1, True),
        (0, 0, False),
        (9999, 0, False),
        (9, 9999, False),
    ],
)
def test_out_of_bounds_sorting_table(
    inventory_map: InventoryMap,
    make_item,
    x: int,
    y: int,
    raises_error: bool,
):
    sorting_table = make_item(name="Sorting table")
    matches = make_item(name="matches")

    check_out_of_bounds = functools.partial(
        inventory_map.check_out_of_bounds,
        matches,
        to=To(id=sorting_table.id, container="hideout", location=Location(x=x, y=y)),
        to_item=sorting_table,
    )
    if raises_error:
        with pytest.raises(OutOfBoundsError):
            check_out_of_bounds()
    else:
        assert check_out_of_bounds() is None
