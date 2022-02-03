from pathlib import Path

import httpx
import orjson
import pytest
from fastapi import status


@pytest.fixture
async def response(http_client: httpx.AsyncClient, language: str) -> httpx.Response:
    return await http_client.post(f"/client/menu/locale/{language}")


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_menu_locale_file(response: httpx.Response, language: str):
    path = Path(f"resources/database/locales/{language}/menu.json")
    assert path.exists()

    with path.open(encoding="utf8") as file:
        locale = orjson.loads(file.read())
    assert response.json()["data"] == locale
