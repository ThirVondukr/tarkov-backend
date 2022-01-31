import pydantic
from pydantic import BaseModel


class AccountCreate(BaseModel):
    class Config:
        allow_population_by_field_name = True

    username: str = pydantic.Field(alias="email")
    password: str
    edition: str
