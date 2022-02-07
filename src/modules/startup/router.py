import datetime
import random
from types import NoneType
from typing import Any

import aiofiles
import orjson
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


@router.post(
    "/client/account/customization",
    response_model=Success[list[str]],
)
async def client_account_customization() -> Success[list[str]]:
    """
    Returns list of all customization id's
    route should not return id's of items that have Node _type, only Item
    """
    available_customization_ids: list[str] = []
    customization_files = paths.customization.glob("*.json")
    for customization_file in customization_files:
        async with aiofiles.open(customization_file) as f:
            contents = orjson.loads(await f.read())
            if contents["_type"] == "Item":
                available_customization_ids.append(contents["_id"])

    return Success(data=available_customization_ids)


@router.post("/client/globals", response_model=Success[dict])
async def client_globals() -> Success[dict]:
    globals_path = paths.base.joinpath("globals.json")
    return Success(data=await read_json_file(globals_path))


@router.post("/client/settings", response_model=Success[dict])
async def client_settings() -> Success[dict]:
    path = paths.base.joinpath("client_settings.json")
    return Success(data=await read_json_file(path))


@router.post("/client/weather", response_model=Success[dict])
async def client_weather() -> Success[dict]:
    weather_file_paths = list(paths.database.joinpath("weather").rglob("*.json"))
    weather = await read_json_file(random.choice(weather_file_paths))

    now = datetime.datetime.now()

    delta = datetime.timedelta(
        hours=now.hour,
        minutes=now.minute,
        seconds=now.second,
        microseconds=now.microsecond,
    )
    accelerated_time = now + delta * weather["acceleration"]
    accelerated_time.replace(
        year=now.year,
        month=now.month,
        day=now.day,
    )

    date_str = accelerated_time.strftime("%Y-%m-%d")
    time_str = accelerated_time.strftime("%H:%M:%S")

    weather["weather"]["timestamp"] = int(now.timestamp())
    weather["weather"]["date"] = date_str
    weather["date"] = date_str

    weather["weather"]["time"] = f"{date_str} {time_str}"
    weather["time"] = time_str

    return Success(data=weather)


@router.post("/client/locations", response_model=Success[dict[str, dict]])
async def client_locations() -> Success[dict[str, dict]]:
    location_bases = paths.database.joinpath("locations", "base").rglob("*.json")
    locations = [await read_json_file(path) for path in location_bases]
    return Success(data={loc["_Id"]: loc for loc in locations})


@router.post(
    "/client/handbook/builds/my/list",
    response_model=Success[list],
)
async def builds_list() -> Success[list]:
    """Route should return list of user builds, currently not implemented"""
    return Success(data=[])


@router.post("/client/server/list", response_model=Success[dict])
async def server_list(request: Request) -> Success[dict]:
    return Success(
        data={
            "ip": utils.server_url(request),
            "port": 443,
        }
    )


@router.post("/client/checkVersion", response_model=Success[dict])
async def check_version() -> Success[dict]:
    return Success(data={"isvalid": True, "latestVersion": ""})
