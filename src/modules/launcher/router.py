import zlib
from typing import Optional

from fastapi import APIRouter, Depends, Request
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
)


@router.get(
    "/launcher/server/connect",
    response_model=schema.ServerInfo,
)
def connect(
    request: Request,
    editions_service: EditionsService = Depends(),
) -> schema.ServerInfo:
    return schema.ServerInfo(
        name=settings.server.name,
        backend_url=str(request.base_url).rstrip("/"),
        editions=editions_service.available_editions,
    )


@router.post("/launcher/profile/register")
async def create_account(
    account_in: AccountCreate,
    account_service: AccountService = Depends(AccountService),
) -> PlainTextResponse:
    if await account_service.is_username_taken(account_in.username):
        return PlainTextResponse(content=zlib.compress("FAILED".encode("utf8")))

    await account_service.create_account(model=account_in)
    return PlainTextResponse(content=zlib.compress("OK".encode("utf8")))


@router.post("/launcher/profile/login")
async def login(
    account_in: AccountLogin,
    account_service: AccountService = Depends(AccountService),
) -> PlainTextResponse:
    user = await account_service.login(account_in)
    if user is None:
        return PlainTextResponse(content=zlib.compress("FAILED".encode("utf8")))
    return PlainTextResponse(content=zlib.compress("OK".encode("utf8")))


@router.post(
    "/launcher/profile/get",
    response_model=AccountSchema,
)
async def get_profile(
    account_in: AccountLogin,
    account_service: AccountService = Depends(AccountService),
) -> Optional[Account]:
    return await account_service.login(account_in)
