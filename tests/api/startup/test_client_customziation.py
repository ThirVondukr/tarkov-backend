import httpx
import orjson
import pytest
from starlette import status

import paths


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post("/client/customization")


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_customization(response: httpx.Response):
    all_customization = {}
    for path in paths.customization.glob("*.json"):
        with path.open(encoding="utf8") as file:
            contents = orjson.loads(file.read())
            all_customization[contents["_id"]] = contents

    assert response.json()["data"] == all_customization
