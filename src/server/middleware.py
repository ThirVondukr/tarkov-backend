from typing import Awaitable, Callable

from starlette.requests import Request
from starlette.responses import Response


async def strip_unity_content_encoding(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    response = await call_next(request)
    if request.headers.get("user-agent", "").startswith("UnityPlayer"):
        del response.headers["content-encoding"]
    return response
