from typing import Any, Callable

from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.routing import APIRoute

from server.requests import ZLibRequest


class ZLibRoute(APIRoute):
    def get_route_handler(self) -> Callable[..., Any]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = ZLibRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler
