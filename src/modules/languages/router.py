from typing import Annotated

from aioinject import Inject
from aioinject.ext.fastapi import inject
from fastapi import APIRouter

from modules.languages.services import LanguageService
from schema import Success
from server import ZLibORJSONResponse, ZLibRoute

router = APIRouter(
    tags=["Languages"],
    route_class=ZLibRoute,
    default_response_class=ZLibORJSONResponse,
)


@router.post(
    "/client/menu/locale/{language}",
    response_model=Success[dict],
)
@inject
async def client_menu_language(
    language: str,
    language_service: Annotated[LanguageService, Inject],
) -> Success[dict]:
    return Success(data=await language_service.menu_locale(language))


@router.post(
    "/client/locale/{language}",
    response_model=Success[dict],
)
@inject
async def client_game_language(
    language: str,
    language_service: Annotated[LanguageService, Inject],
) -> Success[dict]:
    return Success(data=await language_service.client_locale(language))


@router.post(
    "/client/languages",
    response_model=Success[list[dict[str, str]]],
)
@inject
async def client_languages(
    language_service: Annotated[LanguageService, Inject],
) -> Success[list[dict[str, str]]]:
    return Success(data=await language_service.client_languages())
