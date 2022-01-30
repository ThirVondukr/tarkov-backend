from fastapi import APIRouter, Depends, Request

import settings
from launcher.schema import ServerInfo
from launcher.services import EditionsService
from responses import ZLibORJSONResponse

router = APIRouter(
    default_response_class=ZLibORJSONResponse,
)


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
