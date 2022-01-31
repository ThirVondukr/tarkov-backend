from pydantic import BaseModel

import paths


class ServerSettings(BaseModel):
    name = "JET Server"


class DatabaseSettings(BaseModel):
    url = f"sqlite+aiosqlite:///{paths.sqlite_db_path}"
    run_migrations: bool = True


server = ServerSettings()
database = DatabaseSettings()
