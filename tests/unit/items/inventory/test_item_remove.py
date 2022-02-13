from modules.items.actions import To
from modules.items.inventory import Inventory
from modules.items.repository import TemplateRepository
from modules.items.types import Item, Location
from tests.unit.items.conftest import make_item
from utils import generate_id


def test_remove_item(
    template_repository: TemplateRepository,
    inventory: Inventory,
):
    template = template_repository.find(name="car_battery")
    item = Item(
        id=generate_id(),
        template_id=template.id,
    )
    inventory.add_item(
        item=item,
        to=To(id=inventory.root_id, container="hideout", location=Location(x=0, y=0)),
    )

    inventory.remove_item(item)
    assert item.id not in inventory.items


def test_remove_item_roundtrip(
    template_repository: TemplateRepository,
    inventory: Inventory,
):
    template = template_repository.find(name="car_battery")
    for _ in range(5):
        item = Item(
            id=generate_id(),
            template_id=template.id,
        )
        inventory.add_item(
            item=item,
            to=To(
                id=inventory.root_id, container="hideout", location=Location(x=0, y=0)
            ),
        )

        inventory.remove_item(item)


def test_remove_nested(
    template_repository: TemplateRepository,
    inventory: Inventory,
    make_item,
):
    mbss_1 = make_item(name="standartBackpack")
    mbss_2 = make_item(name="standartBackpack")
    car_battery = make_item(name="car_battery")
    inventory.add_item(
        mbss_1,
        to=To(id=inventory.root_id, container="hideout", location=Location(x=0, y=0)),
    )
    inventory.add_item(
        mbss_2,
        to=To(id=mbss_1.id, container="main", location=Location(x=0, y=0)),
    )
    inventory.add_item(
        car_battery, to=To(id=mbss_2.id, container="main", location=Location(x=0, y=0))
    )
    assert len(inventory.items) == 4
    assert len(inventory.taken_locations) == 3

    inventory.remove_item(mbss_1)
    assert len(inventory.items) == 1
    assert mbss_1.id not in inventory.taken_locations
    assert len(inventory.taken_locations) == 1
    assert inventory.root_id in inventory.taken_locations
    assert len(inventory.taken_locations[inventory.root_id]["hideout"]) == 0
