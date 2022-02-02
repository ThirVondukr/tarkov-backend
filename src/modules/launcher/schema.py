import pydantic
from pydantic import BaseModel


class ServerInfo(BaseModel):
    class Config:
        allow_population_by_field_name = True

    name: str
    backend_url: str = pydantic.Field(alias="backendUrl")
    editions: list[str]
