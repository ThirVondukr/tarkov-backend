import modules.items.handlers
from modules.items import handlers
from modules.items.actions import ProfileChanges, Split, To
from modules.items.handlers import Context
from modules.items.inventory import PlayerInventory
from modules.items.types import Location


async def test_split(
    context: Context,
    player_inventory: PlayerInventory,
    make_item,
):
    ammo = make_item(name="patron_9x19_PST_gzh")
    ammo.stack_count = 50
    player_inventory.add_item(
        ammo,
        to=To(
            id=player_inventory.root_id,
            container="hideout",
            location=Location(x=0, y=0),
        ),
    )
    await handlers.split(
        Split(
            item=ammo.id,
            container=To(
                id=player_inventory.root_id,
                container="hideout",
                location=Location(x=0, y=1),
            ),
            count=42,
        ),
        context,
    )
    assert ammo.stack_count == 8
    new_ammo = next(
        item for item in player_inventory.items.values() if item.stack_count == 42
    )
    assert new_ammo.stack_count == 42
