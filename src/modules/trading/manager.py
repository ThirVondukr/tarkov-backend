from __future__ import annotations

import random
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated

from aioinject import Inject

import paths
from modules.items.repository import TemplateRepository
from utils import read_json_file

from .trader import Trader


async def create_trader_manager(
    template_repository: Annotated[TemplateRepository, Inject],
    traders_dir: Path = paths.traders,
) -> TraderManager:
    trader_manager = TraderManager(
        template_repository=template_repository,
        traders_dir=traders_dir,
    )
    for path in traders_dir.iterdir():
        await trader_manager.get(path.stem)
    return trader_manager


class TraderManager:
    RESTOCK_TIME = timedelta(hours=3)

    def __init__(
        self,
        template_repository: TemplateRepository,
        traders_dir: Path,
    ):
        self.traders: dict[str, Trader] = {}
        self._template_repository = template_repository
        self._traders_dir = traders_dir

    async def get(self, trader_id: str) -> Trader:
        if trader_id not in self.traders:
            self.traders[trader_id] = await self._create_trader(trader_id)

        trader = self.traders[trader_id]

        if self._should_refresh_trader(trader):
            self._refresh_trader(trader)

        return trader

    @staticmethod
    def _should_refresh_trader(trader: Trader) -> bool:
        next_resupply: int = trader.base["nextResupply"]
        return int(time.time()) > next_resupply

    def _refresh_trader(self, trader: Trader) -> Trader:
        trader.base["nextResupply"] = (
            datetime.fromtimestamp(trader.base["nextResupply"]) + self.RESTOCK_TIME
        )
        return trader

    async def _create_trader(self, trader_id: str) -> Trader:
        next_resupply = datetime.now() + self.RESTOCK_TIME
        next_resupply -= timedelta(
            seconds=random.gauss(
                self.RESTOCK_TIME.total_seconds() / 2,
                self.RESTOCK_TIME.total_seconds() / 6,
            )
        )

        trader_path = self._traders_dir.joinpath(trader_id)
        trader = Trader(
            base=await read_json_file(trader_path.joinpath("base.json")),
            assort=await read_json_file(trader_path.joinpath("assort.json")),
            categories=await read_json_file(trader_path.joinpath("categories.json")),
            template_repository=self._template_repository,
        )
        trader.base["nextResupply"] = int(next_resupply.timestamp())
        return trader
