from pydantic import BaseModel, field_validator
from typing import Optional

class PartsParameters(BaseModel):
    id:Optional[int] = None
    part_number:Optional[str] = None
    description:Optional[str] = None
    client_name:Optional[str] = None

    @field_validator(
                     "part_number",
                     "description",
                      "client_name",
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value