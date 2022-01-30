import zlib
from typing import Any, Generic, Mapping, TypeVar

from fastapi.responses import ORJSONResponse
from pydantic.generics import GenericModel

T = TypeVar("T")


class SuccessResponse(GenericModel, Generic[T]):
    data: T | None = None
    err: int = 0
    errmsg: str | None = None


class ErrorResponse(GenericModel):
    err: int = True
    errmsg: str | None
    data: Any = None


class ZLibORJSONResponse(ORJSONResponse):
    media_type = "application/json"

    def init_headers(self, headers: Mapping[str, str] | None = None) -> None:
        if not headers:
            headers = {}
        headers["Content-Encoding"] = "deflate"  # type: ignore
        super().init_headers(headers)

    def render(self, content: dict[Any, Any]) -> bytes:
        self.init_headers({"Content-Encoding": "deflate"})
        return zlib.compress(super().render(content))
