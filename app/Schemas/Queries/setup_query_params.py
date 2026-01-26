from pydantic import BaseModel, field_validator
from typing import Optional


class SetupQueryParams(BaseModel):
    machine: str
    part_number: str
    date: str
    Emp_id: str

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