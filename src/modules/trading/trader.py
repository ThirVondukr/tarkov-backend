import itertools
from typing import Any

import pydantic

from modules.items.inventory import Inventory
from modules.items.repository import TemplateRepository
from modules.items.types import Item


class Trader:
    def __init__(
        self,
        base: dict,
        assort: dict[str, Any],
        categories: list[str],
        template_repository: TemplateRepository,
    ):
        self.base = base
        self.assort = assort
        self.categories = categories
        self.inventory = Inventory(
            pydantic.parse_obj_as(
                list[Item],
                list(
                    itertools.chain.from_iterable(
                        assort["items"] for assort in assort.values()
                    )
                ),
            ),
            root_id="hideout",
            template_repository=template_repository,
        )
