from fastapi import APIRouter, Depends

from modules.profile.dependencies import get_profile_id
from modules.profile.types import Profile
from schema import Success
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
