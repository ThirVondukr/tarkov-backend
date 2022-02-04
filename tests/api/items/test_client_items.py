import httpx
import pytest
from starlette import status


@pytest.fixture
async def response(http_client: httpx.AsyncClient) -> httpx.Response:
    return await http_client.post("/client/items")


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_returns_all_items(
    response: httpx.Response,
    templates_as_dict: dict[str, dict],
):
    data = response.json()["data"]
    assert len(data) == len(templates_as_dict)
    for key, item in data.items():
        assert templates_as_dict[key] == item
