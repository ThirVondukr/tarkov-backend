from fastapi import FastAPI

from database import migrations
from modules import items, languages, launcher, profile, singleplayer, startup, trading
from server.middleware import strip_unity_content_encoding


def create_app() -> FastAPI:
    app = FastAPI()
    app.middleware("http")(strip_unity_content_encoding)
    app.include_router(router=items.router)
    app.include_router(router=languages.router)
    app.include_router(router=launcher.router)
    app.include_router(router=profile.router)
    app.include_router(router=singleplayer.router)
    app.include_router(router=startup.router)
    app.include_router(router=trading.router)

    @app.on_event("startup")
    async def on_startup() -> None:
        await migrations.migrate()

    @app.get("/")
    async def hello_world() -> dict[str, str]:
        return {"msg": "Hello World!"}

    return app
