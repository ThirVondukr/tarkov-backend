import contextlib

from sqlalchemy.ext.asyncio import AsyncSession

from .base import Session


@contextlib.asynccontextmanager
async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session
