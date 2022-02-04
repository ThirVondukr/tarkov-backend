from typing import Optional

from fastapi import Cookie, HTTPException
from starlette import status


def get_profile_id(
    session_id: Optional[str] = Cookie(alias="PHPSESSID", default=None),
) -> str:
    if session_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return session_id
