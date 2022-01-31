import asyncio
import uuid

import httpx
import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

import settings
from app import create_app
from database.base import Base, Session

LOCALES = ["ru", "en"]


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return create_app()


@pytest.fixture(scope="session")
def base_url() -> str:
    return "http://test"


@pytest.fixture(scope="session")
async def http_client(app: FastAPI, base_url) -> httpx.AsyncClient:
    async with httpx.AsyncClient(app=app, base_url=base_url) as client:
        yield client


@pytest.fixture
def server_name() -> str:
    old_name = settings.server.name
    settings.server.name = str(uuid.uuid4())
    yield settings.server.name
    settings.server.name = old_name


@pytest.fixture(scope="session")
async def engine() -> AsyncEngine:
    in_memory_url = "sqlite+aiosqlite://"
    settings.database.url = in_memory_url
    return create_async_engine(url=in_memory_url, future=True)


@pytest.fixture(scope="session", autouse=True)
async def create_tables(engine: AsyncEngine):
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=True)
async def session(engine: AsyncEngine) -> AsyncSession:
    async with engine.connect() as conn:
        transaction = await conn.begin()
        Session.configure(bind=conn)

        async with Session() as session:
            yield session

        await transaction.rollback()
