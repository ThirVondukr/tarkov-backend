import operator
from typing import Any

from fastapi import APIRouter

import paths
from modules.trading.types import TraderAssort
from schema import Success
from server import ZLibORJSONResponse, ZLibRoute
from utils import read_json_file

router = APIRouter(
    tags=["Trading"],
    route_class=ZLibRoute,
    default_response_class=ZLibORJSONResponse,
)


@router.post(
    "/client/trading/api/traderSettings",
    response_model=Success[list[dict[str, Any]]],
)
async def trader_settings() -> Success[list[dict[str, Any]]]:
    bases = [await read_json_file(base) for base in paths.traders.rglob("base.json")]
    bases.sort(key=operator.itemgetter("_id"))
    return Success(data=bases)


@router.post(
    "/client/trading/customization/storage",
    response_model=Success[dict],
)
async def customization_storage() -> Success[dict]:
    return Success(data={})


@router.post(
    "/client/trading/api/getTraderAssort/{trader_id}",
    response_model=TraderAssort,
)
async def get_trader_assort(
    trader_id: str,
) -> TraderAssort:
    return TraderAssort()
