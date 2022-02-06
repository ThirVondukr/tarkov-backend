from fastapi import APIRouter, Depends
from starlette.requests import Request

import paths
import utils
from database.models import Account
from modules.profile.dependencies import get_profile_id
from modules.profile.services import ProfileService
from modules.profile.types import Profile
from schema import Error, Success
from server import ZLibORJSONResponse, ZLibRoute
from utils import read_json_file

from ..accounts.dependencies import get_account
from . import schema
from .commands import ProfileCreateCommand
from .schema import ProfileSelect

router = APIRouter(
    default_response_class=ZLibORJSONResponse,
    route_class=ZLibRoute,
    tags=["Profile"],
)


@router.post(
    "/client/game/profile/list",
    response_model=Success[list[Profile]],
)
async def profile_list(
    profile_id: str = Depends(get_profile_id),
    account: Account = Depends(get_account),
) -> Success[list[Profile]]:
    profile_path = paths.profiles.joinpath(profile_id, "character.json")
    if not profile_path.exists() or account.should_wipe:
        return Success(data=[])

    return Success(data=[await read_json_file(profile_path)])


@router.post("/client/game/profile/select", response_model=Success[ProfileSelect])
async def profile_select(request: Request) -> Success[ProfileSelect]:
    return Success(
        data=ProfileSelect(
            notifier=ProfileSelect.Notifier(
                server=utils.server_url(request),
                channel_id="testChannel",
                url="",
                notifier_server="",
                ws="",
            ),
            notifier_server="",
        )
    )


@router.post("/client/profile/status")
async def profile_status(
    account: Account = Depends(get_account),
) -> Success[list[dict]]:
    response = [
        {
            "profileid": f"{profile_type}{account.profile_id}",
            "status": "Free",
            "sid": "",
            "ip": "",
            "port": 0,
        }
        for profile_type in ("scav", "pmc")
    ]
    return Success(data=response)


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


@router.post("/client/game/profile/create", response_model=Success[dict])
async def create_profile(
    profile_create: schema.ProfileCreate,
    account: Account = Depends(get_account),
    command: ProfileCreateCommand = Depends(),
) -> Success[dict]:
    profile = await command.execute(account=account, profile_create=profile_create)
    return Success(data={"uid": profile.id})
