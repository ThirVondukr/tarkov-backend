from modules.items import handlers
from modules.items.actions import Examine, To
from modules.items.handlers import Context
from modules.items.inventory import PlayerInventory
from modules.items.repository import TemplateRepository
from modules.items.types import Location
from modules.profile.types import Profile


async def test_item_examine(
    context: Context,
    player_inventory: PlayerInventory,
    profile: Profile,
    template_repository: TemplateRepository,
    make_item,
):
    item = make_item(name="matches")
    template = template_repository.get(item.template_id)
    player_inventory.add_item(
        item,
        to=To(
            id=player_inventory.root_id,
            container="hideout",
            location=Location(x=0, y=0),
        ),
    )

    assert profile.info.experience == 0
    assert item.template_id not in profile.encyclopedia

    await handlers.examine(
        Examine(item=item.id),
        context,
    )
    assert profile.info.experience == template.props["ExamineExperience"]
    assert profile.encyclopedia[item.template_id] is False

    item1 = make_item(name="matches")
    player_inventory.add_item(
        item1,
        to=To(
            id=player_inventory.root_id,
            container="hideout",
            location=Location(x=1, y=0),
        ),
    )
    await handlers.examine(
        Examine(item=item1.id),
        context,
    )
    assert profile.info.experience == template.props["ExamineExperience"]
    assert profile.encyclopedia[item.template_id] is False
