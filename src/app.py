from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    async def hello_world() -> dict[str, str]:
        return {"msg": "Hello World!"}

    return app
