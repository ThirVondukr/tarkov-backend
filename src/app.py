from aioinject.ext.fastapi import InjectMiddleware
from fastapi import FastAPI

from container import create_container
from database import migrations
from modules import (
    friends,
    hideout,
    items,
    languages,
    launcher,
    mail,
    notifier,
    profile,
    quests,
    singleplayer,
    startup,
    trading,
)
from server.middleware import strip_unity_content_encoding


def create_app() -> FastAPI:
    app = FastAPI()
    app.middleware("http")(strip_unity_content_encoding)
    app.add_middleware(InjectMiddleware, container=create_container())

    app.include_router(router=friends.router)
    app.include_router(router=hideout.router)
    app.include_router(router=items.router)
    app.include_router(router=languages.router)
    app.include_router(router=launcher.router)
    app.include_router(router=mail.router)
    app.include_router(router=notifier.router)
    app.include_router(router=profile.router)
    app.include_router(router=quests.router)
    app.include_router(router=singleplayer.router)
    app.include_router(router=startup.router)
    app.include_router(router=trading.router)

    @app.on_event("startup")
    async def on_startup() -> None:
        await migrations.migrate()

    return app
