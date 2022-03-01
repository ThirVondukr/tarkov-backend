import itertools
import operator
from typing import Annotated, Any

from aioinject import Inject
from aioinject.ext.fastapi import inject
from fastapi import APIRouter

import paths
from modules.trading.manager import TraderManager
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
    response_model=Success[TraderAssort],
)
@inject
async def trader_assort(
    trader_id: str,
    trader_manager: Annotated[TraderManager, Inject],
) -> Success[TraderAssort]:
    trader = await trader_manager.get(trader_id)
    items = itertools.chain.from_iterable(
        assort["items"] for assort in trader.assort.values()
    )
    loyal_level_items = {key: value["loyality"] for key, value in trader.assort.items()}
    barter_scheme = {
        key: value["barter_scheme"] for key, value in trader.assort.items()
    }
    response = TraderAssort(
        barter_scheme=barter_scheme,
        items=list(items),
        loyal_level_items=loyal_level_items,
    )
    return Success(data=response)


@router.post(
    "/client/trading/api/getUserAssortPrice/trader/{trader_id}",
    response_model=Success[dict[str, int]],
)
@inject
async def user_assort_price(
    trader_id: str,
    trader_manager: Annotated[TraderManager, Inject],
) -> Success[dict[str, int]]:
    return Success(data={})
