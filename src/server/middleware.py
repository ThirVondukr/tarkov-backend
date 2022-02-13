import logging
import time
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


async def measure_execution_time(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    start = time.perf_counter()
    result = await call_next(request)
    logging.info(
        "%s Execution time: %s ",
        request.url.path,
        time.perf_counter() - start,
    )
    return result
