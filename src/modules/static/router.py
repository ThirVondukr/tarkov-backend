from fastapi import APIRouter
from fastapi.responses import FileResponse

import paths

router = APIRouter(
    tags=["Static"],
    default_response_class=FileResponse,
)


@router.get("/files/{path:path}")
async def get_file(path: str) -> str:
    path = path.replace("jpg", "png")  # TODO: Maybe think of a better way to do this.
    file = paths.resources.joinpath("static", path)

    if not file.exists():
        raise FileNotFoundError("File does not exist.")

    return str(file)
