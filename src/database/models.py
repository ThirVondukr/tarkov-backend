from typing import cast

from sqlalchemy import BOOLEAN, Column, Integer, String, UniqueConstraint

from utils import generate_id

from .base import Base


class Account(Base):
    __tablename__ = "accounts"
    __table_args__ = (
        UniqueConstraint("username", name="uq_username"),
        UniqueConstraint("profile_nickname", name="uq_profile_nickname"),
        UniqueConstraint("profile_id", name="uq_profile_id"),
    )

    id = Column(Integer, primary_key=True)
    # Launcher Username
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    profile_nickname = Column(String(255), nullable=True)
    edition = Column(String(255), nullable=False)
    should_wipe = Column(BOOLEAN, nullable=False, default=True)

    profile_id = Column(
        String(64),
        nullable=False,
        default=generate_id,
    )

    @property
    def email(self) -> str:
        return cast(str, self.username)
