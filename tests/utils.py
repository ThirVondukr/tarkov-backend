import contextlib
import shutil
import zlib
from pathlib import Path

import httpx


async def deflate_hook(response: httpx.Response) -> None:
    await response.aread()
    contents = response.content
    try:
        response._content = zlib.decompress(contents)
    except zlib.error:
        pass


@contextlib.contextmanager
def tmp_dir(path: Path):
    path.mkdir(exist_ok=True, parents=True)
    yield
    shutil.rmtree(path)
