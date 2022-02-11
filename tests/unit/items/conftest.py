import pytest

from modules.items.inventory import Inventory, Stash
from modules.items.repository import TemplateRepository


@pytest.fixture
def inventory(template_repository: TemplateRepository):
    """
    Standard stash 10x28
    """
    return Inventory.from_container(Stash.standard.value, template_repository)
