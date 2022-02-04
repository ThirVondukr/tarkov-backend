from typing import Any, Literal, Optional

from pydantic import BaseModel, Extra

import utils


class Template(
    BaseModel,
    alias_generator=utils.underscore_prefix,
    extra=Extra.forbid,
):
    id: str
    name: str
    parent: str
    type: Literal["Item", "Node"]
    props: dict[str, Any]
    proto: Optional[str]
