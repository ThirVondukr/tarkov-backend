from fastapi import FastAPI

import paths
import utils
from database import migrations
from modules import items, languages, launcher, singleplayer, startup
from server.middleware import strip_unity_content_encoding


def create_app() -> FastAPI:
    paths.certificates.mkdir(exist_ok=True)
    utils.generate_certificates(paths.certificates)

    app = FastAPI()
    app.middleware("http")(strip_unity_content_encoding)
    app.include_router(router=items.router)
    app.include_router(router=languages.router)
    app.include_router(router=launcher.router)
    app.include_router(router=singleplayer.router)
    app.include_router(router=startup.router)

    @app.on_event("startup")
    async def on_startup() -> None:
        await migrations.migrate()

    @app.get("/")
    async def hello_world() -> dict[str, str]:
        return {"msg": "Hello World!"}

    return app
