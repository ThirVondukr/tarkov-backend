import httpx
import pytest
from starlette import status

from database.models import Account

endpoint_url = "/client/profile/status"


async def test_unauthenticated(http_client: httpx.AsyncClient) -> httpx.Response:
    response = await http_client.post(endpoint_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.fixture
async def response(
    authenticated_http_client: httpx.AsyncClient,
) -> httpx.Response:
    return await authenticated_http_client.post(endpoint_url)


def test_returns_200(response: httpx.Response):
    assert response.status_code == status.HTTP_200_OK


def test_should_return_profile_statuses(
    response: httpx.Response,
    account: Account,
):
    expected = [
        {
            "profileid": f"{profile_type}{account.profile_id}",
            "status": "Free",
            "sid": "",
            "ip": "",
            "port": 0,
        }
        for profile_type in ("scav", "pmc")
    ]
    assert response.json()["data"] == expected
