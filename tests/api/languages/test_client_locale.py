import httpx
import orjson
import pytest
from starlette import status

import paths


@pytest.fixture
async def response(http_client: httpx.AsyncClient, language: str) -> httpx.Response:
    return await http_client.post(f"/client/locale/{language}")


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_locale(response: httpx.Response, language: str):
    with paths.locales.joinpath(language, "locale.json").open(encoding="utf8") as f:
        contents = f.read()
    expected = orjson.loads(contents)
    assert response.json()["data"] == expected
