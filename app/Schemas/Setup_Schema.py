from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

class SetupSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    machine: str
    part_number: str
    Date: datetime
    Emp_id: str
    Notes: Optional[str] = None

    @field_validator("machine",
                     "part_number",
                     "Emp_id", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value