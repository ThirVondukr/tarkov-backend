from fastapi import APIRouter, Depends, Request

import settings
from launcher.schema import ServerInfo
from launcher.services import EditionsService

router = APIRouter()


@router.get(
    "/launcher/server/connect",
    response_model=ServerInfo,
)
def connect(
    request: Request,
    editions_service: EditionsService = Depends(),
) -> ServerInfo:
    return ServerInfo(
        name=settings.server.name,
        backend_url=str(request.base_url).rstrip("/"),
        editions=editions_service.available_editions,
    )
