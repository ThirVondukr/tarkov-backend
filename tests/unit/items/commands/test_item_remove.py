import pytest

from modules.items.actions import ProfileChanges, Remove, To
from modules.items.commands import InventoryActionHandler
from modules.items.inventory import PlayerInventory
from modules.items.types import Location


async def test_remove_single(
    inventory_handler: InventoryActionHandler,
    player_inventory: PlayerInventory,
    profile_changes: ProfileChanges,
    make_item,
):
    matches = make_item(name="matches")
    player_inventory.add_item(
        matches,
        to=To(
            id=player_inventory.root_id,
            container="hideout",
            location=Location(x=0, y=0),
        ),
    )
    amount_of_items_before = len(player_inventory.items)

    await inventory_handler.remove(Remove(item=matches.id))
    with pytest.raises(KeyError):
        player_inventory.get(matches.id)

    assert matches in profile_changes.items.del_
    assert len(player_inventory.items) == amount_of_items_before - 1


async def test_remove_nested(
    inventory_handler: InventoryActionHandler,
    player_inventory: PlayerInventory,
    profile_changes: ProfileChanges,
    make_item,
):
    beta2 = make_item(name="item_equipment_backpack_betav2")
    matches = make_item(name="matches")

    player_inventory.add_item(
        beta2,
        to=To(
            id=player_inventory.root_id,
            container="hideout",
            location=Location(x=0, y=0),
        ),
    )
    player_inventory.add_item(
        matches,
        to=To(
            id=beta2.id,
            container="main",
            location=Location(x=0, y=0),
        ),
    )

    amount_of_items_before = len(player_inventory.items)
    await inventory_handler.remove(Remove(item=beta2.id))

    with pytest.raises(KeyError):
        player_inventory.get(beta2.id)

    with pytest.raises(KeyError):
        player_inventory.get(matches.id)

    assert matches in profile_changes.items.del_
    assert beta2 in profile_changes.items.del_
    assert len(player_inventory.items) == amount_of_items_before - 2
