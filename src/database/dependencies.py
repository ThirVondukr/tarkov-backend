from sqlalchemy.ext.asyncio import AsyncSession

from .base import Session


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session
