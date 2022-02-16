from modules.items.actions import To
from modules.items.inventory import Inventory
from modules.items.repository import TemplateRepository
from modules.items.types import Item, Location
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
    assert len(inventory.map.locations) == 3

    inventory.remove_item(mbss_1)
    assert len(inventory.items) == 1
    assert mbss_1.id not in inventory.map.locations
    assert len(inventory.map.locations) == 1
    assert inventory.root_id in inventory.map.locations
    assert len(inventory.map.locations[inventory.root_id]["hideout"]) == 0


def test_remove_item_from_non_grid_slot(
    inventory: Inventory,
    make_item,
):
    ak = make_item(name="weapon_izhmash_ak74_545x39")
    grip = make_item(name="pistolgrip_ak_us_palm_ak_palm")
    inventory.add_item(
        ak,
        to=To(
            id=inventory.root_id,
            container="hideout",
            location=Location(x=0, y=0),
        ),
    )
    inventory.add_item(grip, to=To(id=ak.id, container="mod_pistol_grip"))
    inventory.remove_item(grip)
    assert inventory.map.locations == {
        inventory.root_id: {"hideout": {(1, 0), (2, 0), (3, 0), (0, 0)}},
    }


def test_remove_ammo(
    inventory: Inventory,
    make_item,
):
    magazine = make_item(name="mag_ak74_izhmash_6L20_545x39_30")
    ammo = make_item(name="patron_545x39_PS")
    inventory.add_item(
        item=magazine,
        to=To(id=inventory.root_id, container="hideout", location=Location(x=0, y=0)),
    )
    inventory.add_item(
        ammo,
        to=To(
            id=magazine.id,
            container="cartridges",
            location=0,
        ),
    )
    inventory.remove_item(ammo)
    assert ammo.id not in inventory.items
    assert inventory.map.cartridges[magazine.id] == set()
