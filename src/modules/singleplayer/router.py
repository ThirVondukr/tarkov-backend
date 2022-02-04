from typing import cast

import yaml
from fastapi import APIRouter
from yaml import CSafeLoader

import paths
from server import ZLibORJSONResponse, ZLibRoute

router = APIRouter(
    default_response_class=ZLibORJSONResponse,
    route_class=ZLibRoute,
)


@router.get("/singleplayer/bundles")
async def singleplayer_bundles() -> list[str]:
    return []


@router.get(
    "/mode/offline",
    response_model=dict[str, bool],
)
def mode_offline() -> dict[str, bool]:
    with paths.config.joinpath("patches.yml").open() as f:
        patches = yaml.load(f, Loader=CSafeLoader)
    return patches  # type: ignore


@router.get(
    "/mode/offlineNodes",
    response_model=dict[str, bool],
)
def mode_offline_nodes() -> dict[str, bool]:
    with paths.config.joinpath("patch_nodes.yml").open() as f:
        return cast(dict[str, bool], yaml.load(f, Loader=CSafeLoader))
