import httpx
import orjson
import pytest
from starlette import status

import paths

endpoint_url = "/client/handbook/templates"


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post(endpoint_url)


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_template_files(response: httpx.Response):
    expected = {}
    for path in paths.database.joinpath("templates").rglob("*.json"):
        with path.open(encoding="utf8") as f:
            expected[path.stem] = orjson.loads(f.read())

    assert response.json()["data"] == expected
