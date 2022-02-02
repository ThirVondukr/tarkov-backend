from typing import Optional

from fastapi import Cookie


def get_profile_id(
    session_id: Optional[str] = Cookie(alias="PHPSESSID", default=None),
) -> str:
    assert session_id
    return session_id
