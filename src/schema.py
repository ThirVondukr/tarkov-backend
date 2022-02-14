import inspect
from typing import Any, Generic, TypeVar, no_type_check

from pydantic import BaseModel, Extra
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


class BaseSchema(BaseModel):
    class Config:
        allow_population_by_field_name = True
        extra = Extra.forbid
        validate_assignment = True

    @no_type_check
    def __setattr__(self, name, value):  # pragma: no cover
        """
        https://github.com/samuelcolvin/pydantic/issues/1577
        """
        try:
            super().__setattr__(name, value)
        except ValueError as e:
            setters = inspect.getmembers(
                self.__class__,
                predicate=lambda x: isinstance(x, property) and x.fset is not None,
            )
            for setter_name, func in setters:
                if setter_name == name:
                    object.__setattr__(self, name, value)
                    break
            else:
                raise e
