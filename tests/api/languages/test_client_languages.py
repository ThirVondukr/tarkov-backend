import httpx
import orjson
import pytest
from fastapi import status

import paths

endpoint_url = "/client/languages"


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post(endpoint_url)


def test_status_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_list_of_language_files(response: httpx.Response):
    locale_files = [
        d.joinpath(f"{d.name}.json") for d in paths.locales.iterdir() if d.is_dir()
    ]
    expected = []
    for locale_file in locale_files:
        with locale_file.open(encoding="utf8") as f:
            expected.append(orjson.loads(f.read()))

    assert response.json() == {"data": expected, "err": 0, "errmsg": None}
