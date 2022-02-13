from typing import Optional

import pytest

from modules.items.inventory import Inventory, Stash
from modules.items.repository import TemplateRepository
from modules.items.types import Item
from utils import generate_id


@pytest.fixture
def inventory(template_repository: TemplateRepository):
    """
    Standard stash 10x28
    """
    return Inventory.from_container(Stash.standard.value, template_repository)


@pytest.fixture
def make_item(template_repository: TemplateRepository):
    def _make_item(
        template_id: str | None = None,
        name: str | None = None,
    ):
        if template_id:
            template = template_repository.get(template_id)
        elif name:
            template = template_repository.find(name=name)
        else:
            raise ValueError

        return Item(
            id=generate_id(),
            template_id=template.id,
        )

    return _make_item
