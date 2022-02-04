import operator
from typing import Any

import aiofiles
import orjson
from fastapi import APIRouter

import paths
from schema import Success
from server import ZLibORJSONResponse, ZLibRoute

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
    bases = []
    for base in paths.traders.rglob("base.json"):
        async with aiofiles.open(base, encoding="utf8") as file:
            bases.append(orjson.loads(await file.read()))
    bases.sort(key=operator.itemgetter("_id"))
    return Success(data=bases)
