from typing import Any

from modules.items.types import Item
from schema import BaseSchema


class TraderAssort(BaseSchema):
    barter_scheme: dict[str, list[list[Any]]] = {}
    items: list[Item] = []
    loyal_level_items: dict = {}
