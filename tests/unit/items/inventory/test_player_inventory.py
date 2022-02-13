from modules.items.inventory import PlayerInventory
from modules.items.repository import TemplateRepository
from modules.profile.types import Profile


def test_can_create_from_profile(
    profile: Profile, template_repository: TemplateRepository
):
    inventory = PlayerInventory.from_profile_inventory(
        profile_inventory=profile.inventory, template_repository=template_repository
    )
    assert inventory
