from fastapi import APIRouter

import paths
from schema import Success
from server import ZLibORJSONResponse, ZLibRoute
from utils import read_json_file

router = APIRouter(
    default_response_class=ZLibORJSONResponse,
    route_class=ZLibRoute,
    tags=["Hideout"],
)


@router.post(
    "/client/hideout/areas",
    response_model=Success[list],
)
async def hideout_areas() -> Success[list]:
    area_files = paths.database.joinpath("hideout", "areas").rglob("*.json")
    return Success(data=[await read_json_file(path) for path in area_files])


@router.post(
    "/client/hideout/settings",
    response_model=Success[dict],
)
async def hideout_settings() -> Success[dict]:
    path = paths.database.joinpath("hideout", "settings.json")
    return Success(data=await read_json_file(path))


@router.post(
    "/client/hideout/production/recipes",
    response_model=Success[list],
)
async def hideout_recipes() -> Success[list]:
    area_files = paths.database.joinpath("hideout", "production").rglob("*.json")
    return Success(data=[await read_json_file(path) for path in area_files])


@router.post(
    "/client/hideout/production/scavcase/recipes",
    response_model=Success[list],
)
async def scavcase_recipes() -> Success[list]:
    recipe_paths = paths.database.joinpath("hideout", "scavcase").rglob("*.json")
    return Success(data=[await read_json_file(path) for path in recipe_paths])
