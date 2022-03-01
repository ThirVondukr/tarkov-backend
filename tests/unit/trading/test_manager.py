from modules.items.repository import TemplateRepository
from modules.trading.manager import TraderManager, create_trader_manager
from modules.trading.trader import Trader


async def test_can_retrieve_traders(
    trader_manager: TraderManager,
    trader_ids: list[str],
):
    for trader_id in trader_ids:
        assert isinstance(await trader_manager.get(trader_id), Trader)


async def test_create_manager(
    trader_ids: list[str],
    template_repository: TemplateRepository,
):
    manager = await create_trader_manager(template_repository)
    for trader_id in trader_ids:
        assert trader_id in manager.traders
