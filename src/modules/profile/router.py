from fastapi import APIRouter, Depends
from starlette.requests import Request

from modules.profile.dependencies import get_profile_id
from modules.profile.services import ProfileService
from modules.profile.types import Profile
from schema import Error, Success
from server import ZLibORJSONResponse, ZLibRoute

router = APIRouter(
    default_response_class=ZLibORJSONResponse,
    route_class=ZLibRoute,
    tags=["Profile"],
)


@router.post(
    "/client/game/profile/list",
    response_model=Success[list | Profile],
)
async def profile_list(
    profile_id: str = Depends(get_profile_id),
) -> Success[list | Profile]:
    return Success(data=[])


@router.post(
    "/client/game/profile/nickname/reserved",
    response_model=Success[str],
)
async def nickname_reserved() -> Success[str]:
    return Success(data="")


@router.post(
    "/client/game/profile/nickname/validate",
    response_model=Success[dict] | Error,
)
async def nickname_validate(
    request: Request,
    profile_service: ProfileService = Depends(),
) -> Success[dict] | Error:
    nickname = (await request.body()).decode()
    if len(nickname) <= 3:
        return Error(err=256, errmsg="The nickname is too short")

    if await profile_service.is_nickname_taken(nickname):
        return Error(err=255, errmsg="The nickname is already in use")

    return Success(data={"status": "ok"})
