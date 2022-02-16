import enum
from collections import defaultdict
from typing import Any, Iterable, NamedTuple, cast

from modules.items.actions import To
from modules.items.repository import TemplateRepository
from modules.items.types import Item, Location, Rotation
from modules.profile.types import Profile
from utils import generate_id


class Stash(enum.Enum):
    edge_of_darkness = "5811ce772459770e9e5f9532"
    prepare_to_escape = "5811ce662459770f6f490f32"
    left_behind = "5811ce572459770cba1a34ea"
    standard = "566abbc34bdc2d92178b4576"


class InventoryError(Exception):
    pass


class OutOfBoundsError(InventoryError):
    pass


class SlotTakenError(InventoryError):
    pass


def iter_children(parent_id: str, items: Iterable[Item]) -> Iterable[Item]:
    if not isinstance(items, list):
        items = list(items)

    stack = [item for item in items if item.parent_id == parent_id]

    while stack:
        child = stack.pop()
        yield child
        stack.extend(item for item in items if item.parent_id == child.id)


class Point(NamedTuple):
    x: int
    y: int


def item_size(
    parent: Item,
    # children: list[Item],
    template_repository: TemplateRepository,
) -> Point:
    template = template_repository.get(parent.template_id)
    width, height = template.props["Width"], template.props["Height"]
    return Point(x=width, y=height)


class InventoryMap:
    def __init__(
        self,
        inventory: "Inventory",
        template_repository: TemplateRepository,
    ):
        self._inventory = inventory
        self._template_repository = template_repository

        self.locations: dict[str, dict[str, set[Point]]] = defaultdict(
            lambda: defaultdict(set)
        )
        self.slots: dict[str, set[str]] = defaultdict(set)
        self.cartridges: dict[str, set[int]] = defaultdict(set)

    def add_item(self, item: Item, to: To) -> None:
        if isinstance(to.location, Location):
            self._check_out_of_bounds(item=item, to=to)
            occupied_locations = self.locations[to.id][to.container]
            for point in self._item_points(item=item, location=to.location):
                if point in occupied_locations:
                    raise SlotTakenError
                occupied_locations.add(point)
        elif isinstance(to.location, int):
            if to.location in self.cartridges[to.id]:
                raise SlotTakenError
            self.cartridges[to.id].add(to.location)
        else:
            if to.container in self.slots[to.id]:
                raise SlotTakenError
            self.slots[to.id].add(to.container)

    def remove_item(
        self,
        item: Item,
        children: list[Item] | None = None,
    ) -> None:
        children = children or []
        assert item.parent_id
        assert item.slot_id

        # Use reverse to remove most nested items first
        for child in reversed(children):
            self.remove_item(child)

        for map_ in [self.locations, self.slots, self.cartridges]:
            map_ = cast(dict[str, Any], map_)
            try:
                del map_[item.id]
            except KeyError:
                pass

        if isinstance(item.location, Location):
            occupied_locations = self.locations[item.parent_id][item.slot_id]
            for point in self._item_points(item=item, location=item.location):
                occupied_locations.remove(point)
        elif isinstance(item.location, int):
            self.cartridges[item.parent_id].remove(item.location)
        else:
            self.slots[item.parent_id].remove(item.slot_id)

    def item_size(self, item: Item, location: Location | None = None) -> Point:
        size = item_size(item, self._template_repository)
        if location is not None and location.rotation is Rotation.Vertical:
            size = Point(x=size.y, y=size.x)
        return size

    def _check_out_of_bounds(self, item: Item, to: To) -> None:
        assert isinstance(to.location, Location)
        if to.location.x < 0 or to.location.y < 0:
            raise OutOfBoundsError

        container_width, container_height = self._template_repository.container_size(
            self._inventory.get(to.id).template_id, slot=to.container
        )

        item_x, item_y = self.item_size(item, location=to.location)
        if to.location.x + item_x > container_width:
            raise OutOfBoundsError

        if to.location.y + item_y > container_height:
            raise OutOfBoundsError

    def _item_points(self, item: Item, location: Location) -> Iterable[Point]:
        size = self.item_size(item, location)
        for x in range(location.x, location.x + size.x):
            for y in range(location.y, location.y + size.y):
                yield Point(x=x, y=y)


class Inventory:
    def __init__(
        self,
        items: list[Item],
        root_id: str,
        template_repository: TemplateRepository,
    ):
        self.items = {item.id: item for item in items}
        self.root_id = root_id
        self.tpl_repository = template_repository
        self.map = InventoryMap(self, template_repository)

    @classmethod
    def from_container(
        cls,
        container_template_id: str,
        template_repository: TemplateRepository,
    ) -> "Inventory":
        container = Item(
            id=generate_id(),
            template_id=container_template_id,
        )
        return cls(
            items=[container],
            root_id=container.id,
            template_repository=template_repository,
        )

    def get(self, item_id: str) -> Item:
        return self.items[item_id]

    def children(self, parent: Item, include_self: bool) -> Iterable[Item]:
        children = iter_children(parent.id, self.items.values())

        if include_self:
            yield parent

        yield from children

    def add_item(self, item: Item, to: To) -> None:
        if item.id in self.items:
            raise ValueError

        self.items[item.id] = item
        item.location = to.location
        item.slot_id = to.container
        item.parent_id = to.id

        self.map.add_item(item, to)

    def remove_item(self, item: Item) -> None:
        children = list(self.children(item, include_self=False))
        self.map.remove_item(item, children)

        del self.items[item.id]
        for child in self.children(item, include_self=False):
            del self.items[child.id]

    def split(self, item: Item, to: To, count: int) -> Item:
        if count <= 0:
            raise ValueError

        if item.stack_count <= count:
            raise ValueError
        item.stack_count -= count

        new_item = item.copy(deep=True)
        new_item.id = generate_id()
        new_item.stack_count = count
        self.add_item(
            new_item,
            to=to,
        )
        return new_item


class PlayerInventory(Inventory):
    def __init__(
        self,
        items: list[Item],
        template_repository: TemplateRepository,
        root_id: str,
        equipment_id: str,
        quest_raid_items_id: str,
        quest_stash_items_id: str,
        sorting_table_id: str,
    ):
        super().__init__(
            items=items, root_id=root_id, template_repository=template_repository
        )
        self.equipment_id = equipment_id
        self.quest_raid_items_id = quest_raid_items_id
        self.quest_stash_items_id = quest_stash_items_id
        self.sorting_table_id = sorting_table_id

    @classmethod
    def from_profile_inventory(
        cls,
        profile_inventory: Profile.Inventory,
        template_repository: TemplateRepository,
    ) -> "PlayerInventory":
        root_ids = {
            profile_inventory.stash,
            profile_inventory.equipment,
            profile_inventory.quest_raid_items,
            profile_inventory.quest_stash_items,
            profile_inventory.sorting_table,
        }
        root_items = [i for i in profile_inventory.items if i.id in root_ids]
        assert len(root_items) == len(root_ids)

        inventory = cls(
            items=root_items,
            template_repository=template_repository,
            root_id=profile_inventory.stash,
            equipment_id=profile_inventory.equipment,
            quest_raid_items_id=profile_inventory.quest_raid_items,
            quest_stash_items_id=profile_inventory.quest_stash_items,
            sorting_table_id=profile_inventory.sorting_table,
        )
        for root_id in root_ids:
            for child in iter_children(root_id, profile_inventory.items):
                inventory.add_item(
                    item=child,
                    to=To(
                        id=child.parent_id,
                        container=child.slot_id,
                        location=child.location,
                    ),
                )
        return inventory
