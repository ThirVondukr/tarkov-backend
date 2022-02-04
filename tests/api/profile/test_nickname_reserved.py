import httpx


async def test_should_return_empty_str(http_client: httpx.AsyncClient):
    response = await http_client.post("/client/game/profile/nickname/reserved")
    assert response.json() == {"data": "", "err": 0, "errmsg": None}
