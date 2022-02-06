import httpx
import orjson
import pytest
from starlette import status

import paths

endpoint_url = "/client/locations"


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post(endpoint_url)


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_all_location_bases(response: httpx.Response):
    expected = {}
    for path in paths.database.joinpath("locations", "base").rglob("*.json"):
        with path.open(encoding="utf8") as f:
            location = orjson.loads(f.read())
            expected[location["_Id"]] = location

    assert response.json()["data"] == expected
