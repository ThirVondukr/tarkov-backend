import pytest

from modules.items.actions import To
from modules.items.inventory import Inventory
from modules.items.repository import TemplateRepository
from modules.items.types import Item, Location
from utils import generate_id


@pytest.fixture
def car_battery(template_repository: TemplateRepository):
    return Item(
        id=generate_id(),
        template_id=template_repository.find(name="car_battery").id,
    )


@pytest.fixture
def mbss(template_repository: TemplateRepository):
    return Item(
        id=generate_id(),
        template_id=template_repository.find(name="standartBackpack").id,
    )


@pytest.fixture
def inventory(inventory: Inventory, mbss, car_battery):
    inventory.add_item(
        item=mbss,
        to=To(id=inventory.root_id, container="hideout", location=Location(x=0, y=0)),
    )

    inventory.add_item(
        item=car_battery,
        to=To(id=mbss.id, container="main", location=Location(x=0, y=0)),
    )

    return inventory


def test_iter_children(
    template_repository: TemplateRepository, inventory: Inventory, mbss, car_battery
):
    stash = inventory.get(inventory.root_id)
    assert list(inventory.children(stash, include_self=False)) == [mbss, car_battery]


def test_iter_children_including_self(
    template_repository: TemplateRepository, inventory: Inventory, mbss, car_battery
):
    assert list(inventory.children(mbss, include_self=True)) == [mbss, car_battery]
