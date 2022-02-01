from typing import Any, Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class Success(GenericModel, Generic[T]):
    data: T | None = None
    err: int = 0
    errmsg: str | None = None


class Error(GenericModel):
    err: int = True
    errmsg: str | None
    data: Any = None
