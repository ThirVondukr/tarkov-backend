import httpx
import pytest
from starlette import status

endpoint_url = "/client/repeatalbeQuests/activityPeriods"


@pytest.fixture
async def response(authenticated_http_client: httpx.AsyncClient) -> httpx.Response:
    return await authenticated_http_client.post(endpoint_url)


def test_status_ok(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_should_return_stub_data(response: httpx.Response):
    assert response.json()["data"] == []
