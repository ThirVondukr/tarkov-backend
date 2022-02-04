from fastapi import APIRouter, Depends

from modules.languages.services import LanguageService
from schema import Success
from server import ZLibORJSONResponse, ZLibRoute

router = APIRouter(
    tags=["Languages"],
    route_class=ZLibRoute,
    default_response_class=ZLibORJSONResponse,
)


@router.post("/client/menu/locale/{language}")
async def client_menu_language(
    language: str,
    language_service: LanguageService = Depends(),
) -> Success[dict]:
    return Success(data=await language_service.menu_locale(language))


@router.post("/client/locale/{language}")
async def client_game_language(
    language: str,
    language_service: LanguageService = Depends(),
) -> Success[dict]:
    return Success(data=await language_service.client_locale(language))


@router.post("/client/languages")
async def client_languages(
    language_service: LanguageService = Depends(),
) -> Success[list[str]]:
    return Success(data=language_service.available_languages())