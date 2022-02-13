import itertools

import pytest

from modules.items.actions import To
from modules.items.inventory import Inventory, OutOfBoundsError, SlotTakenError
from modules.items.repository import TemplateRepository
from modules.items.types import Item, Location, Rotation
from utils import generate_id


def test_can_add_item(
    template_repository: TemplateRepository,
    inventory: Inventory,
):
    item = Item(
        id=generate_id(),
        template_id=template_repository.find(name="item_barter_flam_propane").id,
    )
    inventory.add_item(
        item,
        to=To(
            id=inventory.root_id,
            container="hideout",
            location=Location(x=0, y=0),
        ),
    )

    assert item.parent_id == inventory.root_id
    assert item.slot_id == "hideout"
    assert item.location == Location(x=0, y=0)

    assert inventory.items[item.id] == item
    assert len(inventory.items) == 2


def test_add_twice(
    template_repository: TemplateRepository,
    inventory: Inventory,
):
    item = Item(
        id=generate_id(),
        template_id=template_repository.find(name="item_barter_flam_propane").id,
    )
    inventory.add_item(
        item,
        to=To(
            id=inventory.root_id,
            container="hideout",
            location=Location(x=0, y=0),
        ),
    )
    with pytest.raises(ValueError):
        inventory.add_item(
            item,
            to=To(
                id=inventory.root_id,
                container="hideout",
                location=Location(x=0, y=0),
            ),
        )


@pytest.mark.parametrize(
    "x,y,rotation",
    [
        (-1, 0, Rotation.Horizontal),
        (0, -1, Rotation.Horizontal),
        (8, 0, Rotation.Horizontal),
        (9, 0, Rotation.Horizontal),
        (10, 0, Rotation.Horizontal),
        (0, 27, Rotation.Horizontal),
        (0, 26, Rotation.Vertical),
    ],
)
def test_out_of_bounds(
    template_repository: TemplateRepository,
    inventory: Inventory,
    x: int,
    y: int,
    rotation: Rotation,
):
    """
    Basic out of bounds check,
    items shouldn't be moved out of inventory/container bounds
    """
    item = Item(
        id=generate_id(),
        template_id=template_repository.find(name="car_battery").id,
    )
    with pytest.raises(OutOfBoundsError):
        inventory.add_item(
            item,
            to=To(
                id=inventory.root_id,
                container="hideout",
                location=Location(
                    x=x,
                    y=y,
                    rotation=rotation,
                ),
            ),
        )


def test_check_edges(
    template_repository: TemplateRepository,
    inventory: Inventory,
):
    """
    Try to place item along inventory edge
    """
    template = template_repository.find(name="matches")
    size_x, size_y = template_repository.container_size(
        inventory.get(inventory.root_id).template_id,
        slot="hideout",
    )
    # Just a lazy way to generate points on inventory edges
    points = list(itertools.product(range(size_x), range(size_y)))
    points = [(x, y) for x, y in points if x in (0, size_x - 1) or y in (0, size_y - 1)]
    assert len(points) == size_y * 2 + size_x * 2 - 4

    for x, y in points:
        inventory.add_item(
            Item(
                id=generate_id(),
                template_id=template.id,
            ),
            to=To(
                id=inventory.root_id,
                container="hideout",
                location=Location(x=x, y=y),
            ),
        )


def test_multiple_items_in_same_location(
    template_repository: TemplateRepository,
    inventory: Inventory,
):
    template = template_repository.find(name="matches")

    inventory.add_item(
        item=Item(
            id=generate_id(),
            template_id=template.id,
        ),
        to=To(id=inventory.root_id, container="hideout", location=Location(x=0, y=0)),
    )
    with pytest.raises(SlotTakenError):
        inventory.add_item(
            item=Item(
                id=generate_id(),
                template_id=template.id,
            ),
            to=To(
                id=inventory.root_id, container="hideout", location=Location(x=0, y=0)
            ),
        )


@pytest.mark.parametrize(
    "x,y,rotation",
    [
        (5, 5, Rotation.Horizontal),
        (6, 5, Rotation.Horizontal),
        (7, 5, Rotation.Horizontal),
        (5, 4, Rotation.Horizontal),
        (5, 4, Rotation.Vertical),
        (5, 3, Rotation.Vertical),
    ],
)
def test_items_intersecting(
    template_repository: TemplateRepository,
    inventory: Inventory,
    x: int,
    y: int,
    rotation: Rotation,
):
    template = template_repository.find(name="car_battery")

    inventory.add_item(
        item=Item(
            id=generate_id(),
            template_id=template.id,
        ),
        to=To(id=inventory.root_id, container="hideout", location=Location(x=5, y=5)),
    )
    with pytest.raises(SlotTakenError):
        inventory.add_item(
            item=Item(
                id=generate_id(),
                template_id=template.id,
            ),
            to=To(
                id=inventory.root_id,
                container="hideout",
                location=Location(
                    x=x,
                    y=y,
                    rotation=rotation,
                ),
            ),
        )


def test_add_item_into_nested_inventory(
    template_repository: TemplateRepository,
    inventory: Inventory,
):
    mbss_tpl = template_repository.find(name="standartBackpack")
    car_tpl = template_repository.find(name="car_battery")

    mbss = Item(
        id=generate_id(),
        template_id=mbss_tpl.id,
    )
    car_battery_1 = Item(
        id=generate_id(),
        template_id=car_tpl.id,
    )
    car_battery_2 = Item(
        id=generate_id(),
        template_id=car_tpl.id,
    )

    inventory.add_item(
        mbss,
        to=To(id=inventory.root_id, container="hideout", location=Location(x=0, y=10)),
    )
    inventory.add_item(
        car_battery_1,
        to=To(id=inventory.root_id, container="hideout", location=Location(x=0, y=0)),
    )
    inventory.add_item(
        car_battery_2, to=To(id=mbss.id, container="main", location=Location(x=0, y=0))
    )


@pytest.mark.parametrize(
    "x,y,rotation",
    [
        (-1, 0, Rotation.Horizontal),
        (0, -1, Rotation.Horizontal),
        (2, 0, Rotation.Horizontal),
        (0, 2, Rotation.Vertical),
    ],
)
def test_place_nested_out_of_bounds(
    template_repository: TemplateRepository,
    inventory: Inventory,
    x: int,
    y: int,
    rotation: Rotation,
):
    mbss = Item(
        id=generate_id(),
        template_id=template_repository.find(name="standartBackpack").id,
    )
    car_battery = Item(
        id=generate_id(),
        template_id=template_repository.find(name="car_battery").id,
    )

    inventory.add_item(
        mbss,
        to=To(id=inventory.root_id, container="hideout", location=Location(x=0, y=0)),
    )
    with pytest.raises(OutOfBoundsError):
        inventory.add_item(
            car_battery,
            to=To(
                id=mbss.id,
                container="main",
                location=Location(x=x, y=y, rotation=rotation),
            ),
        )


def test_add_item_to_different_slots(
    inventory: Inventory,
    make_item,
):
    pockets = make_item(name="карманы 2 на 2")
    matches = [make_item(name="matches") for _ in range(4)]

    inventory.add_item(
        pockets,
        to=To(id=inventory.root_id, container="hideout", location=Location(x=0, y=0)),
    )
    for i, item in enumerate(matches, start=1):
        inventory.add_item(
            item,
            to=To(id=pockets.id, container=f"pocket{i}", location=Location(x=0, y=0)),
        )


def test_add_item_to_non_grid_slot(
    inventory: Inventory,
    make_item,
):
    ak = make_item(name="weapon_izhmash_ak74_545x39")
    grip = make_item(name="pistolgrip_ak_us_palm_ak_palm")
    inventory.add_item(
        ak,
        to=To(
            id=inventory.root_id,
            container="hideout",
            location=Location(x=0, y=0),
        ),
    )
    inventory.add_item(grip, to=To(id=ak.id, container="mod_pistol_grip"))
    assert "mod_pistol_grip" in inventory.taken_locations[ak.id]
    with pytest.raises(SlotTakenError):
        inventory.add_item(
            item=make_item(name="pistolgrip_ak_us_palm_ak_palm"),
            to=To(
                id=ak.id,
                container="mod_pistol_grip",
            ),
        )
    inventory.remove_item(grip)
    inventory.add_item(grip, to=To(id=ak.id, container="mod_pistol_grip"))
