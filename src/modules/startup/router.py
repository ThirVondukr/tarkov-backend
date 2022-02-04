from types import NoneType
from typing import Any

from fastapi import APIRouter, Depends, Request

import paths
import utils
from modules.languages.services import LanguageService
from schema import Success
from server import ZLibORJSONResponse, ZLibRoute
from utils import read_json_file

from ..profile.dependencies import get_profile_id
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


@router.post(
    "/client/customization",
    response_model=Success[dict[str, Any]],
)
async def client_customization() -> Success[dict[str, Any]]:
    customization = {}
    customization_files = paths.customization.glob("*.json")
    for customization_file in customization_files:
        contents = await read_json_file(customization_file)
        customization[contents["_id"]] = contents

    return Success(data=customization)


@router.post("/client/globals", response_model=Success[dict])
async def client_globals() -> Success[dict]:
    globals_path = paths.base.joinpath("globals.json")
    return Success(data=await read_json_file(globals_path))


@router.post("/client/settings", response_model=Success[dict])
async def client_settings() -> Success[dict]:
    path = paths.base.joinpath("client_settings.json")
    return Success(data=await read_json_file(path))
