from pydantic import BaseModel, field_validator
from typing import Optional


class RelationParameters(BaseModel):
    id: Optional[int] = None
    create_item_part_number: Optional[str] = None
    consume_item_part_number: Optional[str] = None


    @field_validator("create_item_part_number",
                     "consume_item_part_number", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value