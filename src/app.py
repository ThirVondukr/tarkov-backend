from pathlib import Path

from fastapi import FastAPI

import launcher
import paths
import startup
import utils


def create_app() -> FastAPI:
    paths.certificates.mkdir(exist_ok=True)
    utils.generate_certificates(paths.certificates)

    app = FastAPI()
    app.include_router(router=startup.router)
    app.include_router(router=launcher.router)

    @app.get("/")
    async def hello_world() -> dict[str, str]:
        return {"msg": "Hello World!"}

    return app
