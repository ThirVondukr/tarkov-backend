import pytest

import paths
from modules.items.repository import TemplateRepository
from modules.trading.manager import TraderManager


@pytest.fixture
def trader_manager(
    template_repository: TemplateRepository,
):
    return TraderManager(
        template_repository=template_repository,
        traders_dir=paths.traders,
    )


@pytest.fixture
def trader_ids() -> list[str]:
    return list(path.stem for path in paths.traders.iterdir())
