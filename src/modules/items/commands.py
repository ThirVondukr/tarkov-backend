import functools
from typing import Awaitable, Callable

from modules.items.actions import (
    Action,
    Move,
    ProfileChanges,
    ReadEncyclopedia,
    Remove,
    To,
)
from modules.items.inventory import PlayerInventory
from modules.items.repository import TemplateRepository
from modules.profile.types import Profile


class ActionHandler:
    actions_map: dict[type[Action], Callable[[Action], Awaitable[None]]]

    @functools.cached_property
    def actions(self) -> tuple[type[Action], ...]:
        return tuple(self.actions_map)

    async def execute(self, action: Action) -> None:
        await self.actions_map[type(action)](action)


class ReadEncyclopediaHandler(ActionHandler):
    def __init__(self, encyclopedia: dict[str, bool]) -> None:
        self.encyclopedia = encyclopedia
        self.actions_map = {
            ReadEncyclopedia: self.read_encyclopedia,
        }

    async def read_encyclopedia(self, action: ReadEncyclopedia) -> None:
        for template_id in action.ids:
            self.encyclopedia[template_id] = True


class InventoryActionHandler(ActionHandler):
    def __init__(
        self,
        inventory: PlayerInventory,
        profile_changes: ProfileChanges,
    ):
        self.inventory = inventory
        self.profile_changes = profile_changes
        self.actions_map = {
            Move: self.move,
            Remove: self.remove,
        }

    async def move(self, action: Move) -> None:
        item = self.inventory.get(action.item)
        children = list(self.inventory.children(item, include_self=False))
        self.inventory.remove_item(item)

        self.inventory.add_item(item, to=action.to)
        for child in children:
            self.inventory.add_item(
                item=child,
                to=To(
                    id=child.parent_id, container=child.slot_id, location=child.location
                ),
            )
        self.profile_changes.items.change.append(item)

    async def remove(self, action: Remove) -> None:
        item = self.inventory.get(action.item)

        for child in self.inventory.children(item, include_self=True):
            self.profile_changes.items.del_.append(child)

        self.inventory.remove_item(item)


class ActionExecutor:
    def __init__(
        self,
        profile: Profile,
        template_repository: TemplateRepository,
    ):
        self.profile = profile
        self.inventory = PlayerInventory.from_profile_inventory(
            profile_inventory=profile.inventory,
            template_repository=template_repository,
        )

    async def execute(self, actions: list[Action]) -> ProfileChanges:
        profile_changes = ProfileChanges(
            skills=self.profile.skills,
        )
        handlers: list[ActionHandler] = [
            ReadEncyclopediaHandler(self.profile.encyclopedia),
            InventoryActionHandler(
                inventory=self.inventory,
                profile_changes=profile_changes,
            ),
        ]

        for action in actions:
            for handler in handlers:
                if isinstance(action, handler.actions):
                    await handler.execute(action)
                    break
            else:
                raise Exception("Action not handled", action)

        self.profile.inventory.items = list(self.inventory.items.values())
        return profile_changes
