import pydantic
from pydantic import BaseModel


class AccountCreate(BaseModel):
    class Config:
        allow_population_by_field_name = True

    username: str = pydantic.Field(alias="email")
    password: str
    edition: str


class AccountLogin(BaseModel):
    class Config:
        allow_population_by_field_name = True

    username: str = pydantic.Field(alias="email")
    password: str


class AccountSchema(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True

    id: int
    username: str = pydantic.Field(alias="nickname")
    email: str
    password: str
    edition: str
    should_wipe: bool = pydantic.Field(alias="wipe")
