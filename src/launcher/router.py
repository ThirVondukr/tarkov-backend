from fastapi import APIRouter, Request, Depends

import settings
from launcher.services import EditionsService

router = APIRouter()


@router.get("/launcher/server/connect")
def connect(
    request: Request,
    editions_service: EditionsService = Depends(),
):
    return {
        "name": settings.server.name,
        "backendUrl": str(request.base_url).rstrip("/"),
        "editions": editions_service.available_editions,
    }
