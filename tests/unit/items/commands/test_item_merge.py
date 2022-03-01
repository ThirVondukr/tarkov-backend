import pytest

from modules.items import handlers
from modules.items.actions import Merge, ProfileChanges, To
from modules.items.handlers import Context
from modules.items.inventory import PlayerInventory
from modules.items.types import Location


async def test_merge(
    context: Context,
    player_inventory: PlayerInventory,
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

    await handlers.merge(
        Merge(
            item=ammo_2.id,
            with_=ammo_1.id,
        ),
        context,
    )
    with pytest.raises(KeyError):
        player_inventory.get(ammo_2.id)

    assert ammo_1.stack_count == 30


async def test_cant_merge_different_items(
    context: Context,
    player_inventory: PlayerInventory,
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
        await handlers.merge(
            Merge(
                item=ammo_2.id,
                with_=ammo_1.id,
            ),
            context,
        )


async def test_cant_merge_items_exceeding_max_stack(
    context: Context,
    player_inventory: PlayerInventory,
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
        await handlers.merge(
            Merge(
                item=ammo_2.id,
                with_=ammo_1.id,
            ),
            context,
        )
