import enum
from collections import defaultdict
from typing import Iterable

from modules.items.actions import To
from modules.items.repository import TemplateRepository
from modules.items.types import Item, Location, Rotation
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
        self.taken_locations: dict[str, set[tuple[int, int]]] = defaultdict(set)

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

    def _check_out_of_bounds(self, item: Item, to: To) -> None:
        if to.location.x < 0 or to.location.y < 0:
            raise OutOfBoundsError

        container_width, container_height = self.tpl_repository.container_size(
            self.get(to.id).template_id, slot=to.container
        )

        item_x, item_y = self.item_size(item, location=to.location)
        if to.location.x + item_x > container_width:
            raise OutOfBoundsError

        if to.location.y + item_y > container_height:
            raise OutOfBoundsError

    def _item_points(self, item: Item, location: Location) -> Iterable[tuple[int, int]]:
        width, height = self.item_size(item, location)
        for x in range(location.x, location.x + width):
            for y in range(location.y, location.y + height):
                yield x, y

    def children(self, parent: Item, include_self: bool) -> Iterable[Item]:
        stack = [item for item in self.items.values() if item.parent_id == parent.id]
        if include_self:
            yield parent
        while stack:
            child = stack.pop()
            yield child
            stack.extend(
                item for item in self.items.values() if item.parent_id == child.id
            )

    def item_size(
        self, item: Item, location: Location | None = None
    ) -> tuple[int, int]:
        template = self.tpl_repository.get(item.template_id)
        width, height = template.props["Width"], template.props["Height"]
        if location is not None and location.rotation is Rotation.Vertical:
            width, height = height, width
        return width, height

    def add_item(self, item: Item, to: To) -> None:
        self._check_out_of_bounds(item=item, to=to)

        self.items[item.id] = item
        item.location = to.location
        item.slot_id = to.container
        item.parent_id = to.id

        for point in self._item_points(item=item, location=to.location):
            if point in self.taken_locations[to.id]:
                raise SlotTakenError
            self.taken_locations[to.id].add(point)

    def remove_item(self, item: Item) -> None:

        del self.items[item.id]
        for point in self._item_points(item=item, location=item.location):
            self.taken_locations[item.parent_id].remove(point)
            try:
                del self.taken_locations[item.id]
            except KeyError:
                pass

        for child in self.children(item, include_self=False):
            del self.items[child.id]
            if child.id in self.taken_locations:
                del self.taken_locations[child.id]
