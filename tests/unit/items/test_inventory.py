import itertools

import pytest

from modules.items.actions import To
from modules.items.inventory import Inventory, OutOfBoundsError, SlotTakenError
from modules.items.repository import TemplateRepository
from modules.items.types import Item, Location, Rotation
from utils import generate_id


def test_can_create(inventory):
    assert inventory


def test_can_move_item(
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
            location=Location(
                x=0,
                y=0,
            ),
        ),
    )

    assert item.parent_id == inventory.root_id
    assert item.slot_id == "hideout"
    assert item.location == Location(x=0, y=0)

    assert inventory.items[item.id] == item
    assert len(inventory.items) == 2


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
