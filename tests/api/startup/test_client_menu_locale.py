from pathlib import Path
from typing import NamedTuple

import httpx
import orjson
import pytest
from fastapi import status

from tests.conftest import LOCALES


class LocaleResponse(NamedTuple):
    response: httpx.Response
    locale: str


@pytest.fixture(params=LOCALES)
async def response(http_client: httpx.AsyncClient, request) -> LocaleResponse:
    response = await http_client.post(f"/client/game/locale/{request.param}")
    return LocaleResponse(response, request.param)


def test_returns_200(response: LocaleResponse):
    assert response.response.status_code == status.HTTP_200_OK


def test_returns_menu_locale_file(response: LocaleResponse):
    path = Path(f"resources/database/locales/{response.locale}/menu.json")
    assert path.exists()

    with path.open(encoding="utf8") as file:
        locale = orjson.loads(file.read())
    assert response.response.json()["data"] == locale
