from pathlib import Path

from fastapi import FastAPI

import launcher
import startup
import utils


def create_app() -> FastAPI:
    certs_directory = Path("resources/certs")
    certs_directory.mkdir(exist_ok=True)
    utils.generate_certificates(certs_directory)

    app = FastAPI()
    app.include_router(router=startup.router)
    app.include_router(router=launcher.router)

    @app.get("/")
    async def hello_world() -> dict[str, str]:
        return {"msg": "Hello World!"}

    return app
