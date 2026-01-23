from pydantic import BaseModel, field_validator
from typing import Optional

class EmployersParameters(BaseModel):
    id:Optional[int] = None
    name:Optional[str] = None
    emp_id:Optional[str] = None

    @field_validator(
                     "name",
                     "emp_id",
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value