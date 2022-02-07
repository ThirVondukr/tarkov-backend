import aiofiles
import orjson
from fastapi import APIRouter

import paths
from schema import Success
from server import ZLibORJSONResponse, ZLibRoute

router = APIRouter(
    default_response_class=ZLibORJSONResponse,
    route_class=ZLibRoute,
    tags=["Quests"],
)


@router.post(
    "/client/quest/list",
    response_model=Success[list],
)
async def quest_list() -> Success[list]:
    path = paths.database.joinpath("quests", "quests.json")
    async with aiofiles.open(path, encoding="utf8") as f:
        return Success(data=orjson.loads(await f.read()))


@router.post(
    "/client/repeatalbeQuests/activityPeriods",
    response_model=Success[list],
)
async def repeatable_quests() -> Success[list]:
    return Success(data=[])
