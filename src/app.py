from fastapi import FastAPI

import paths
import utils
from database import migrations
from modules import languages, launcher, singleplayer, startup


def create_app() -> FastAPI:
    paths.certificates.mkdir(exist_ok=True)
    utils.generate_certificates(paths.certificates)

    app = FastAPI()
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
