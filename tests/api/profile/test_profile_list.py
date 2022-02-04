import uuid

import httpx
from starlette import status

url = "/client/game/profile/list"


async def test_no_session_id(
    http_client: httpx.AsyncClient,
):
    """
    Should raise 401 Unauthorized if no session_id is provided
    """
    response = await http_client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_profile_is_not_created_yet(http_client: httpx.AsyncClient):
    """
    Should return empty list if profile is not yet created
    """
    session_id = str(uuid.uuid4())
    response = await http_client.post(url, cookies={"PHPSESSID": session_id})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == []
