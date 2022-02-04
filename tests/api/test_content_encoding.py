import httpx


async def test_returns_content_encoding_header(http_client: httpx.AsyncClient):
    response = await http_client.post("/client/game/keepalive")
    assert response.headers["content-encoding"] == "deflate"


async def test_does_not_return_contend_encoding_for_unity_client(
    unity_client: httpx.AsyncClient,
):
    response = await unity_client.post("/client/game/keepalive")
    assert "content_encoding" not in response.headers
