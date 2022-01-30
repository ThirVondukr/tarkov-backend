import time

import aiofiles
import orjson
from fastapi import APIRouter

from responses import SuccessResponse

router = APIRouter(tags=["Startup"])


@router.post("/client/game/start")
def client_game_start() -> SuccessResponse[dict]:
    data = {"utc_time": int(time.time() / 1000)}
    return SuccessResponse(data=data)


@router.post("/client/game/locale/{locale}")
async def client_game_locale(locale: str) -> SuccessResponse[dict]:
    path = f"resources/database/locales/{locale}/menu.json"
    async with aiofiles.open(path, encoding="utf8") as file:
        contents = await file.read()
    return SuccessResponse(data=orjson.loads(contents))
