from fastapi import FastAPI

import launcher
import startup


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(router=startup.router)
    app.include_router(router=launcher.router)

    @app.get("/")
    async def hello_world() -> dict[str, str]:
        return {"msg": "Hello World!"}

    return app
