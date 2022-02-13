import pytest

from modules.items.actions import To
from modules.items.inventory import Inventory
from modules.items.types import Item, Location


@pytest.fixture
def ammo(make_item, template_repository) -> Item:
    ammo_ = make_item(name="patron_9x19_PST_gzh")
    ammo_.upd["StackObjectsCount"] = 50
    return ammo_


@pytest.fixture
def inventory(inventory: Inventory, ammo: Item):
    inventory.add_item(
        item=ammo,
        to=To(id=inventory.root_id, container="hideout", location=Location(x=0, y=0)),
    )
    return inventory


def test_split(inventory: Inventory, ammo: Item):
    new_item = inventory.split(
        ammo,
        to=To(id=inventory.root_id, container="hideout", location=Location(x=1, y=0)),
        count=5,
    )
    assert ammo.id != new_item.id
    assert new_item.upd["StackObjectsCount"] == 5
    assert new_item.location == Location(x=1, y=0)


@pytest.mark.parametrize("count", [0, -1])
def test_split_negative_amount(inventory: Inventory, ammo: Item, count: int):
    with pytest.raises(ValueError):
        inventory.split(
            ammo,
            to=To(
                id=inventory.root_id,
                container="hideout",
                location=Location(x=1, y=0),
            ),
            count=count,
        )


@pytest.mark.parametrize("count", [50, 51])
def test_split_more_than_stack(inventory: Inventory, ammo: Item, count: int):
    with pytest.raises(ValueError):
        inventory.split(
            ammo,
            to=To(
                id=inventory.root_id,
                container="hideout",
                location=Location(x=1, y=0),
            ),
            count=count,
        )
