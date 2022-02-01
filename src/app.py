from fastapi import FastAPI

import launcher
import paths
import startup
import utils
from database import migrations


def create_app() -> FastAPI:
    paths.certificates.mkdir(exist_ok=True)
    utils.generate_certificates(paths.certificates)

    app = FastAPI()
    app.include_router(router=startup.router)
    app.include_router(router=launcher.router)

    @app.on_event("startup")
    async def on_startup() -> None:
        await migrations.migrate()

    @app.get("/")
    async def hello_world() -> dict[str, str]:
        return {"msg": "Hello World!"}

    return app
