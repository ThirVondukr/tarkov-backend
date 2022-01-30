import time

from fastapi import APIRouter

from responses import SuccessResponse

router = APIRouter(tags=["Startup"])


@router.post("/client/game/start")
def client_game_start() -> SuccessResponse[dict]:
    data = {"utc_time": int(time.time() / 1000)}
    return SuccessResponse(data=data)
