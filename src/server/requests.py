import zlib

from fastapi.requests import Request
from starlette.datastructures import MutableHeaders


class ZLibRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            try:
                self._body = zlib.decompress(body)
                headers = MutableHeaders(raw=self.scope["headers"])
                headers["Content-Length"] = str(len(self._body))
            except zlib.error:
                self._body = body
        return self._body
