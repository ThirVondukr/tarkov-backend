from __future__ import annotations

import dataclasses
from typing import Annotated, Any, Awaitable, Callable, Type

from aioinject import Inject
from starlette.background import BackgroundTasks

from modules.items.actions import (
    Action,
    AnyAction,
    ApplyInventoryChanges,
    Examine,
    Merge,
    Move,
    Owner,
    ProfileChanges,
    ReadEncyclopedia,
    Remove,
    Split,
    To,
    Transfer,
)
from modules.items.inventory import Inventory, PlayerInventory
from modules.items.repository import TemplateRepository
from modules.items.types import Item
from modules.profile.services import ProfileManager
from modules.profile.types import Profile
from modules.trading.manager import TraderManager


async def read_encyclopedia(action: ReadEncyclopedia, ctx: Context) -> None:
    for template_id in action.ids:
        ctx.profile.encyclopedia[template_id] = True


async def examine(action: Examine, ctx: Context) -> None:
    item = ctx.from_inventory.get(action.item)
    template = ctx.template_repository.get(item.template_id)
    if template.id not in ctx.profile.encyclopedia:
        ctx.profile.info.experience += template.props["ExamineExperience"]
    ctx.profile.encyclopedia[template.id] = False


async def move(action: Move, ctx: Context) -> None:
    item = ctx.from_inventory.get(action.item)
    children = list(ctx.from_inventory.children(item, include_self=False))
    ctx.from_inventory.remove_item(item)

    ctx.inventory.add_item(item, to=action.to)
    for child in children:
        ctx.inventory.add_item(
            item=child,
            to=To(id=child.parent_id, container=child.slot_id, location=child.location),
        )
    ctx.profile_changes.items.change.append(item)


async def remove(action: Remove, ctx: Context) -> None:
    item = ctx.inventory.get(action.item)

    for child in ctx.inventory.children(item, include_self=True):
        ctx.profile_changes.items.del_.append(child)

    ctx.inventory.remove_item(item)


async def split(action: Split, ctx: Context) -> None:
    # TODO Account for multiple inventories
    item = ctx.inventory.get(action.item)
    new_item = ctx.inventory.split(
        item,
        to=action.container,
        count=action.count,
    )
    ctx.profile_changes.items.new.append(new_item)


async def merge(action: Merge, ctx: Context) -> None:
    # TODO: Account for multiple inventories
    item = ctx.inventory.get(item_id=action.item)
    target = ctx.inventory.get(item_id=action.with_)

    if item.template_id != target.template_id:
        raise ValueError

    max_stack_size = ctx.template_repository.get(item.template_id).props["StackMaxSize"]
    if item.stack_count + target.stack_count > max_stack_size:
        raise ValueError

    target.stack_count += item.stack_count
    ctx.inventory.remove_item(item)
    ctx.profile_changes.items.del_.append(item)
    ctx.profile_changes.items.change.append(target)


async def transfer(action: Transfer, ctx: Context) -> None:
    # TODO: Account for multiple inventories
    if action.count <= 0:
        raise ValueError

    item = ctx.inventory.get(item_id=action.item)
    target = ctx.inventory.get(item_id=action.with_)
    if item.template_id != target.template_id:
        raise ValueError
    max_stack_size = ctx.template_repository.get(item.template_id).props["StackMaxSize"]
    if target.stack_count + action.count > max_stack_size:
        raise ValueError
    target.stack_count += action.count
    item.stack_count -= action.count

    ctx.profile_changes.items.change.extend([item, target])


async def apply_inventory_changes(action: ApplyInventoryChanges, ctx: Context) -> None:
    items: list[Item] = []

    for changed_item in action.changed_items:
        item = ctx.inventory.get(changed_item.id)
        items.append(item)
        items.extend(ctx.inventory.children(item, include_self=False))
        ctx.inventory.remove_item(item)

        item.parent_id = changed_item.parent_id
        item.slot_id = changed_item.slot_id
        item.location = changed_item.location

    for item in items:
        ctx.inventory.add_item(item, to=To.from_item(item))


@dataclasses.dataclass
class Context:
    profile: Profile
    inventory: Inventory
    from_inventory: Inventory
    profile_changes: ProfileChanges

    template_repository: TemplateRepository


class ActionHandler:
    def __init__(
        self,
        profile_manager: Annotated[ProfileManager, Inject],
        trader_manager: Annotated[TraderManager, Inject],
        template_repository: Annotated[TemplateRepository, Inject],
    ):
        self.profile_manager = profile_manager
        self.trader_manager = trader_manager
        self.template_repository = template_repository

    @property
    def handlers(
        self,
    ) -> dict[Type[Action], Callable[[Any, Context], Awaitable[None]]]:
        return {
            ReadEncyclopedia: read_encyclopedia,
            Examine: examine,
            Move: move,
            Remove: remove,
            Split: split,
            Merge: merge,
            Transfer: transfer,
            ApplyInventoryChanges: apply_inventory_changes,
        }

    async def execute(
        self,
        actions: list[AnyAction],
        profile_id: str,
        background_tasks: BackgroundTasks | None = None,
    ) -> ProfileChanges:
        async with self.profile_manager.profile(
            profile_id=profile_id, background_tasks=background_tasks
        ) as profile:
            profile_changes = ProfileChanges(
                skills=profile.skills,
            )
            inventory = PlayerInventory.from_profile_inventory(
                profile_inventory=profile.inventory,
                template_repository=self.template_repository,
            )
            for action in actions:
                context = Context(
                    profile=profile,
                    inventory=inventory,
                    from_inventory=await self.inventory_from(
                        action.from_owner, inventory
                    ),
                    profile_changes=profile_changes,
                    template_repository=self.template_repository,
                )
                handler = self.handlers[type(action)]
                await handler(action, context)

            profile.inventory.items = list(inventory.items.values())
            return profile_changes

    async def inventory_from(
        self,
        owner: Owner | None,
        player_inventory: PlayerInventory,
    ) -> Inventory:
        if owner is None:
            return player_inventory

        if owner.type == "Trader":
            trader = await self.trader_manager.get(owner.id)
            return trader.inventory
        raise NotImplementedError
