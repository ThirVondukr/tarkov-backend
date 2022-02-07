from fastapi import APIRouter

from schema import Success
from server import ZLibORJSONResponse, ZLibRoute

router = APIRouter(
    default_response_class=ZLibORJSONResponse,
    route_class=ZLibRoute,
    tags=["Mail"],
)


@router.post(
    "/client/mail/dialog/list",
    response_model=Success[list],
)
async def dialog_list() -> Success[list]:
    return Success(data=[])
