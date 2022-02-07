from fastapi import APIRouter

from schema import Success
from server import ZLibORJSONResponse, ZLibRoute

from .schema import FriendListSchema

router = APIRouter(
    default_response_class=ZLibORJSONResponse,
    route_class=ZLibRoute,
    tags=["Friends"],
)


@router.post(
    "/client/friend/list",
    response_model=Success[FriendListSchema],
)
async def friend_list() -> Success[FriendListSchema]:
    return Success(
        data=FriendListSchema(
            friends=[],
            ignore=[],
            in_ignore_list=[],
        )
    )
