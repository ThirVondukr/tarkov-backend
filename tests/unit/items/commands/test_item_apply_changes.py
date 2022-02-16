import copy

from modules.items.actions import ApplyInventoryChanges, To
from modules.items.commands import InventoryActionHandler
from modules.items.inventory import PlayerInventory
from modules.items.types import Location


async def test_apply_inventory_changes(
    inventory_handler: InventoryActionHandler,
    player_inventory: PlayerInventory,
    make_item,
):
    items = [
        make_item(name="matches") for _ in range(3)
    ]
    for i, item in enumerate(items):
        player_inventory.add_item(
            item,
            to=To(
                id=player_inventory.root_id,
                container="hideout",
                location=Location(x=i, y=0)
            )
        )

    changed_items = copy.deepcopy(items)
    for item in changed_items:
        item.location.x = len(changed_items) - 1 - item.location.x

    action = ApplyInventoryChanges(
        changed_items=changed_items,
    )
    await inventory_handler.apply_inventory_changes(action)

    for item, changed_item in zip(items, changed_items):
        assert item.location == changed_item.location
