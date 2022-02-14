import pytest

from modules.items.actions import Merge, ProfileChanges, To
from modules.items.commands import InventoryActionHandler
from modules.items.inventory import PlayerInventory
from modules.items.types import Location


async def test_merge(
    inventory_handler: InventoryActionHandler,
    player_inventory: PlayerInventory,
    profile_changes: ProfileChanges,
    make_item,
):
    ammo_1 = make_item(name="patron_9x19_PST_gzh", stack_count=10)
    ammo_2 = make_item(name="patron_9x19_PST_gzh", stack_count=20)

    for i, item in enumerate([ammo_1, ammo_2]):
        player_inventory.add_item(
            item,
            to=To(
                id=player_inventory.root_id,
                container="hideout",
                location=Location(x=i, y=0),
            ),
        )

    await inventory_handler.merge(
        Merge(
            item=ammo_2.id,
            with_=ammo_1.id,
        )
    )
    with pytest.raises(KeyError):
        player_inventory.get(ammo_2.id)

    assert ammo_1.stack_count == 30


async def test_cant_merge_different_items(
    inventory_handler: InventoryActionHandler,
    player_inventory: PlayerInventory,
    profile_changes: ProfileChanges,
    make_item,
):
    ammo_1 = make_item(name="patron_9x19_PST_gzh", stack_count=10)
    ammo_2 = make_item(name="patron_9x18pm_SP8_gzh", stack_count=20)

    for i, item in enumerate([ammo_1, ammo_2]):
        player_inventory.add_item(
            item,
            to=To(
                id=player_inventory.root_id,
                container="hideout",
                location=Location(x=i, y=0),
            ),
        )
    with pytest.raises(ValueError):
        await inventory_handler.merge(
            Merge(
                item=ammo_2.id,
                with_=ammo_1.id,
            )
        )


async def test_cant_merge_items_exceeding_max_stack(
    inventory_handler: InventoryActionHandler,
    player_inventory: PlayerInventory,
    profile_changes: ProfileChanges,
    make_item,
):
    ammo_1 = make_item(name="patron_9x19_PST_gzh", stack_count=25)
    ammo_2 = make_item(name="patron_9x19_PST_gzh", stack_count=26)

    for i, item in enumerate([ammo_1, ammo_2]):
        player_inventory.add_item(
            item,
            to=To(
                id=player_inventory.root_id,
                container="hideout",
                location=Location(x=i, y=0),
            ),
        )
    with pytest.raises(ValueError):
        await inventory_handler.merge(
            Merge(
                item=ammo_2.id,
                with_=ammo_1.id,
            )
        )
