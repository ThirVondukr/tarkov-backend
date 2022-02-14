import pytest

from modules.items.actions import ProfileChanges
from modules.items.commands import InventoryActionHandler
from modules.items.inventory import PlayerInventory
from modules.items.repository import TemplateRepository
from modules.profile.types import Profile


@pytest.fixture
def player_inventory(
    template_repository: TemplateRepository, make_item
) -> PlayerInventory:
    stash = make_item(name="Edge of darkness stash 10x68")
    equipment = make_item(name="Default Inventory")
    quest_raid = make_item(name="stash 8x6")
    quest_stash = make_item(name="stash 8x6")
    sorting_table = make_item(name="Sorting table")
    inventory = Profile.Inventory(
        stash=stash.id,
        equipment=equipment.id,
        quest_raid_items=quest_raid.id,
        quest_stash_items=quest_stash.id,
        sorting_table=sorting_table.id,
        fast_panel={},
        items=[stash, equipment, quest_raid, quest_stash, sorting_table],
    )
    return PlayerInventory.from_profile_inventory(
        profile_inventory=inventory,
        template_repository=template_repository,
    )


@pytest.fixture
def profile_changes() -> ProfileChanges:
    return ProfileChanges(skills={})


@pytest.fixture
def inventory_handler(
    player_inventory: PlayerInventory,
    profile_changes: ProfileChanges,
    template_repository: TemplateRepository,
) -> InventoryActionHandler:
    return InventoryActionHandler(
        inventory=player_inventory,
        profile_changes=profile_changes,
        template_repository=template_repository,
    )
