from fastapi import APIRouter
from server import ZLibRoute, FileResponse

from os.path import exists

import paths

router = APIRouter(
    tags=["Static"],
    route_class=ZLibRoute,
    default_response_class=FileResponse,
)


@router.get(
    "/files/{path:path}",
    response_class=FileResponse
)
async def get_file(path: str) -> str:
    path = path.replace('jpg', 'png')  # TODO: Maybe think of a better way to do this.
    file = paths.resources.joinpath("static", path)

    if not exists(file):
        raise FileNotFoundError("File does not exist.")

    return file
