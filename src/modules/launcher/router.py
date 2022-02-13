import zlib
from typing import Annotated, Optional

from aioinject import Inject
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse

import settings
from database.models import Account
from modules.accounts.schema import AccountCreate, AccountLogin, AccountSchema
from modules.accounts.services import AccountService
from modules.launcher.services import EditionsService
from server import ZLibORJSONResponse, ZLibRoute

from . import schema

router = APIRouter(
    default_response_class=ZLibORJSONResponse,
    route_class=ZLibRoute,
    tags=["Launcher"],
)


@router.get(
    "/launcher/server/connect",
    response_model=schema.ServerInfo,
)
@inject
async def connect(
    request: Request,
    editions_service: Annotated[EditionsService, Inject],
) -> schema.ServerInfo:
    return schema.ServerInfo(
        name=settings.server.name,
        backend_url=str(request.base_url).rstrip("/"),
        editions=editions_service.available_editions,
    )


@router.post("/launcher/profile/register")
@inject
async def create_account(
    account_in: AccountCreate,
    account_service: Annotated[AccountService, Inject],
) -> PlainTextResponse:
    if await account_service.is_username_taken(account_in.username):
        return PlainTextResponse(content=zlib.compress("FAILED".encode("utf8")))

    await account_service.create_account(model=account_in)
    return PlainTextResponse(content=zlib.compress("OK".encode("utf8")))


@router.post("/launcher/profile/login")
@inject
async def login(
    account_in: AccountLogin,
    account_service: Annotated[AccountService, Inject],
) -> PlainTextResponse:
    user = await account_service.login(account_in)
    if user is None:
        return PlainTextResponse(content=zlib.compress("FAILED".encode("utf8")))
    return PlainTextResponse(content=zlib.compress("OK".encode("utf8")))


@router.post(
    "/launcher/profile/get",
    response_model=AccountSchema,
)
@inject
async def get_profile(
    account_in: AccountLogin,
    account_service: Annotated[AccountService, Inject],
) -> Optional[Account]:
    return await account_service.login(account_in)
