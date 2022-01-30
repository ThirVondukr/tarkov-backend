from fastapi import FastAPI

from startup import router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(router=router)

    @app.get("/")
    async def hello_world() -> dict[str, str]:
        return {"msg": "Hello World!"}

    return app
