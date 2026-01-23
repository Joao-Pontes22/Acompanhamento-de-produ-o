from pydantic import BaseModel, field_validator
from typing import Optional


class ComponentsParameters(BaseModel):
    id:Optional[int] = None
    part_number:Optional[str] = None
    description:Optional[str] = None
    supplier_name:Optional[str] = None
    component_type:Optional[str] = None

    @field_validator(
                     "part_number",
                     "description",
                      "supplier_name",
                      "component_type",
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

