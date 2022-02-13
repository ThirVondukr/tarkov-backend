import zlib
from typing import Any, Mapping

from fastapi.responses import ORJSONResponse


class ZLibORJSONResponse(ORJSONResponse):
    media_type = "application/json"

    def init_headers(
        self, headers: Mapping[str, str] | None = None
    ) -> None:  # pragma: no cover
        if not headers:
            headers = {}
        headers["Content-Encoding"] = "deflate"  # type: ignore
        super().init_headers(headers)

    def render(self, content: dict[Any, Any]) -> bytes:
        return zlib.compress(super().render(content))
