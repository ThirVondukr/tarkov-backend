import asyncio
import itertools
import uuid

import httpx
import orjson
import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

import paths
import settings
from app import create_app
from database.base import Base, Session
from database.models import Account


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


@pytest.fixture
async def account(session: AsyncSession) -> Account:
    account = Account(
        username=str(uuid.uuid4()),
        password="Password",
        edition="Standard",
    )
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account


@pytest.fixture(params=["ru", "en"])
def language(request) -> str:
    return request.param


@pytest.fixture(scope="session")
def templates() -> list[dict]:
    contents = []
    for file in paths.items.glob("*.json"):
        with file.open(encoding="utf8") as f:
            contents.append(orjson.loads(f.read()))
    return list(itertools.chain.from_iterable(contents))


@pytest.fixture(scope="session")
def templates_as_dict(templates) -> dict[str, dict]:
    return {tpl["_id"]: tpl for tpl in templates}
