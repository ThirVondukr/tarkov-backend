import pytest

from modules.items.actions import ProfileChanges, To, Transfer
from modules.items.commands import InventoryActionHandler
from modules.items.inventory import PlayerInventory
from modules.items.types import Location


@pytest.fixture
def item_1(make_item):
    return make_item(name="patron_9x19_PST_gzh", stack_count=40)


@pytest.fixture
def item_2(make_item):
    return make_item(name="patron_9x19_PST_gzh", stack_count=40)


@pytest.fixture
def player_inventory(player_inventory: PlayerInventory, item_1, item_2):
    for i, item in enumerate([item_1, item_2]):
        player_inventory.add_item(
            item,
            to=To(
                id=player_inventory.root_id,
                container="hideout",
                location=Location(x=i, y=0),
            ),
        )
    return player_inventory


async def test_transfer(
    inventory_handler: InventoryActionHandler,
    profile_changes: ProfileChanges,
    item_1,
    item_2,
):
    await inventory_handler.transfer(
        Transfer(
            item=item_1.id,
            with_=item_2.id,
            count=10,
        )
    )
    assert item_1.stack_count == 30
    assert item_2.stack_count == 50

    assert item_1 in profile_changes.items.change
    assert item_2 in profile_changes.items.change


async def test_transfer_exceeding_max_stack(
    inventory_handler: InventoryActionHandler,
    item_1,
    item_2,
):
    with pytest.raises(ValueError):
        await inventory_handler.transfer(
            Transfer(item=item_1.id, with_=item_2.id, count=11)
        )


async def test_transfer_different_items(
    player_inventory: PlayerInventory,
    inventory_handler: InventoryActionHandler,
    item_1,
    make_item,
):
    item_2 = make_item(name="matches")
    player_inventory.add_item(
        item_2,
        to=To(
            id=player_inventory.root_id,
            container="hideout",
            location=Location(x=0, y=1),
        ),
    )
    with pytest.raises(ValueError):
        await inventory_handler.transfer(
            Transfer(item=item_1.id, with_=item_2.id, count=1)
        )


@pytest.mark.parametrize(
    "count",
    (-1, 0),
)
async def test_transfer_negative_amount(
    inventory_handler: InventoryActionHandler,
    item_1,
    item_2,
    count: int,
):
    with pytest.raises(ValueError):
        await inventory_handler.transfer(
            Transfer(item=item_1.id, with_=item_2.id, count=count)
        )
