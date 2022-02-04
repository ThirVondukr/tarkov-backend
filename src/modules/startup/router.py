from types import NoneType

from fastapi import APIRouter, Depends, Request

import utils
from dependencies import get_profile_id
from modules.languages.services import LanguageService
from schema import Success
from server import ZLibORJSONResponse, ZLibRoute

from . import schema

router = APIRouter(
    tags=["Startup"],
    route_class=ZLibRoute,
    default_response_class=ZLibORJSONResponse,
)


@router.post("/client/game/start")
async def client_game_start() -> Success[dict]:
    data = {"utc_time": utils.timestamp()}
    return Success(data=data)


@router.post("/client/game/version/validate")
async def client_game_version_validate() -> Success[NoneType]:
    return Success()


@router.post("/client/game/config")
async def client_game_config(
    request: Request,
    profile_id: str = Depends(get_profile_id),
    language_service: LanguageService = Depends(),
) -> Success[schema.ClientGameConfig]:
    config = schema.ClientGameConfig(
        aid=profile_id,
        token=profile_id,
        active_profile_id=f"user{profile_id}pmc",
        nickname="user",
        languages=await language_service.languages(),
        backend=schema.Backend.from_root_url(
            utils.server_url(request),
        ),
    )
    return Success(data=config)


@router.post(
    "/client/game/keepalive",
    response_model=Success[dict[str, str]],
)
async def keepalive() -> Success[dict[str, str]]:
    return Success(data={"msg": "ok"})
