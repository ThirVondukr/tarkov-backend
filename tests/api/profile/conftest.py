import httpx
import pytest
from starlette import status

from database.models import Account


@pytest.fixture
async def profile(
    account: Account,
    authenticated_http_client: httpx.AsyncClient,
    profile_dir,
    freeze_time,
):
    response = await authenticated_http_client.post(
        "/client/game/profile/create",
        json={
            "side": "Usec",
            "nickname": account.username,
            "headId": "",
            "voiceId": "",
        },
    )
    assert response.status_code == status.HTTP_200_OK
