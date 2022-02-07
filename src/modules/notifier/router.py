from fastapi import APIRouter, Depends, Request

import utils
from modules.profile.dependencies import get_profile_id
from schema import Success
from server import ZLibORJSONResponse, ZLibRoute

router = APIRouter(
    default_response_class=ZLibORJSONResponse,
    route_class=ZLibRoute,
    tags=["Notifier"],
)


@router.post(
    "/client/notifier/channel/create",
    response_model=Success[dict],
)
async def channel_create(
    request: Request, profile_id: str = Depends(get_profile_id)
) -> Success[dict]:
    data = {
        "notifier": {
            "server": utils.server_url(request),
            "channel_id": "testChannel",
            "url": request.url_for("channel_get", profile_id=profile_id),
        },
        "notifierServer": request.url_for("channel_get", profile_id=profile_id),
    }
    return Success(data=data)


@router.post("/client/notifier/channel/{profile_id}")
async def channel_get(profile_id: str) -> None:
    pass
