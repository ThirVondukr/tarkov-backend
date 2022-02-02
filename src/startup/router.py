import time

import aiofiles
import orjson
from fastapi import APIRouter

from schema import Success

router = APIRouter(tags=["Startup"])


@router.post("/client/game/start")
def client_game_start() -> Success[dict]:
    data = {"utc_time": utils.timestamp()}
    return Success(data=data)


@router.post("/client/game/locale/{locale}")
async def client_game_locale(locale: str) -> Success[dict]:
    path = f"resources/database/locales/{locale}/menu.json"
    async with aiofiles.open(path, encoding="utf8") as file:
        contents = await file.read()
    return Success(data=orjson.loads(contents))
