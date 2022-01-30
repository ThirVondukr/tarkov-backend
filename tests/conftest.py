import httpx
import pytest
from fastapi import FastAPI

from app import create_app

LOCALES = ["ru", "en"]

@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest.fixture
async def http_client(app: FastAPI) -> httpx.AsyncClient:
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client
