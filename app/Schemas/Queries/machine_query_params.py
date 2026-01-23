from pydantic import BaseModel, field_validator
from typing import Optional

class MachineParameters(BaseModel):
    id: Optional[int] = None 
    machine: Optional[str] = None

    @field_validator(
                     "machine",
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

