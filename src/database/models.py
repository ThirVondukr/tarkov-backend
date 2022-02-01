from typing import cast

from sqlalchemy import BOOLEAN, Column, Integer, String

from .base import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    edition = Column(String(255), nullable=False)
    should_wipe = Column(BOOLEAN, nullable=False, default=True)

    profile_id = Column(String(64), nullable=True, unique=True)

    @property
    def email(self) -> str:
        return cast(str, self.username)
