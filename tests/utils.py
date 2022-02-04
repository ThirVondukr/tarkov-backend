import zlib

import httpx


async def deflate_hook(response: httpx.Response) -> None:
    await response.aread()
    contents = response.content
    try:
        response._content = zlib.decompress(contents)
    except zlib.error:
        pass
