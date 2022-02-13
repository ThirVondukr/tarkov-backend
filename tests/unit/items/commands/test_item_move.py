from modules.items.actions import Move, ProfileChanges, To
from modules.items.commands import InventoryActionHandler
from modules.items.inventory import PlayerInventory
from modules.items.types import Location


async def test_simple_move(
    make_item,
    player_inventory: PlayerInventory,
    inventory_handler: InventoryActionHandler,
    profile_changes: ProfileChanges,
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
    assert matches.location == Location(x=0, y=0)
    await inventory_handler.move(
        Move(
            item=matches.id,
            to=To(
                id=player_inventory.root_id,
                container="hideout",
                location=Location(x=0, y=5),
            ),
        )
    )
    assert matches.location == Location(x=0, y=5)
    assert matches in profile_changes.items.change
    assert len(profile_changes.items.del_) == 0
    assert len(profile_changes.items.new) == 0


async def test_simple_move_with_children(
    make_item,
    player_inventory: PlayerInventory,
    inventory_handler: InventoryActionHandler,
    profile_changes: ProfileChanges,
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
        matches, to=To(id=beta2.id, container="main", location=Location(x=0, y=0))
    )
    assert beta2.location == Location(x=0, y=0)
    assert matches.parent_id == beta2.id
    assert matches.location == Location(x=0, y=0)

    await inventory_handler.move(
        Move(
            item=beta2.id,
            to=To(
                id=player_inventory.root_id,
                container="hideout",
                location=Location(x=0, y=5),
            ),
        )
    )
    assert beta2.location == Location(x=0, y=5)

    assert len(profile_changes.items.change) == 1
    assert beta2 in profile_changes.items.change

    assert len(profile_changes.items.del_) == 0
    assert len(profile_changes.items.new) == 0
