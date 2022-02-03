import httpx
import pytest
from fastapi import status

import paths

endpoint_url = "/client/languages"


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post(endpoint_url)


def test_status_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_list_of_available_languages(response: httpx.Response):
    locales = [dir.name for dir in paths.locales.iterdir() if dir.is_dir()]
    assert response.json() == {"data": locales, "err": 0, "errmsg": None}
