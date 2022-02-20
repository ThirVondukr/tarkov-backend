import asyncio
import itertools
import pathlib
import shutil
import time
import uuid

import httpx
import orjson
import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from starlette import status

import paths
import settings
from app import create_app
from database.base import Base, Session
from database.models import Account
from modules.items.repository import TemplateRepository, create_template_repository
from modules.profile.services import ProfileManager
from modules.profile.types import Profile
from tests.utils import deflate_hook


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
    return "https://test"


@pytest.fixture(scope="session")
async def http_client(app: FastAPI, base_url) -> httpx.AsyncClient:
    client = httpx.AsyncClient(
        app=app,
        base_url=base_url,
        event_hooks={"response": [deflate_hook]},
    )
    async with client:
        yield client


@pytest.fixture
async def authenticated_http_client(app: FastAPI, base_url: str, account: Account):
    client = httpx.AsyncClient(
        app=app,
        base_url=base_url,
        event_hooks={"response": [deflate_hook]},
        cookies={
            "PHPSESSID": account.profile_id,
        },
    )
    async with client:
        yield client


@pytest.fixture
async def unity_client(app: FastAPI, base_url) -> httpx.AsyncClient:
    unity_user_agent = (
        "UnityPlayer/2019.1.14f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)"
    )
    client = httpx.AsyncClient(
        app=app,
        base_url=base_url,
        event_hooks={"response": [deflate_hook]},
        headers={
            "user-agent": unity_user_agent,
        },
    )
    async with client:
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


@pytest.fixture
def profile_dir(account: Account) -> pathlib.Path:
    profile_path = paths.profiles.joinpath(account.profile_id)
    profile_path.mkdir(exist_ok=True)
    yield profile_path
    shutil.rmtree(profile_path)


@pytest.fixture
def profile_manager() -> ProfileManager:
    return ProfileManager()


@pytest.fixture
async def create_profile(
    account: Account,
    authenticated_http_client: httpx.AsyncClient,
    profile_dir,
    profile_manager: ProfileManager,
):
    response = await authenticated_http_client.post(
        "/client/game/profile/create",
        json={
            "side": "Usec",
            "nickname": account.username,
            "headId": "",
            "voiceId": "",
        },
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.fixture
async def profile(
    profile_manager: ProfileManager, account: Account, create_profile
) -> Profile:
    async with profile_manager.profile(
        account.profile_id,
        readonly=True,
    ) as profile:
        yield profile


@pytest.fixture(params=["ru", "en", "fr", "ge"])
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


@pytest.fixture
def freeze_time() -> float:
    original_time_function = time.time
    timestamp = original_time_function()

    time.time = lambda: timestamp
    yield timestamp
    time.time = original_time_function


@pytest.fixture(scope="session")
async def template_repository() -> TemplateRepository:
    return await create_template_repository()
