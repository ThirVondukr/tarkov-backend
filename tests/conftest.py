import asyncio
import uuid

import httpx
import pytest
from fastapi import FastAPI

import settings
from app import create_app

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
