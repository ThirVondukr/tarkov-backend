from pydantic import BaseModel


class ServerSettings(BaseModel):
    name = "JET Server"


server = ServerSettings()
