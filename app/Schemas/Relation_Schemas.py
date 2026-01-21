from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class RelationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    create_item_part_number: str
    consume_item_part_number: str
    qnty: int


    @field_validator("create_item_part_number",
                     "consume_item_part_number", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value


class UpdateRelationInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    create_item_part_number: Optional[str] 
    consume_item_part_number: Optional[str] 
    qnty: Optional[int] 


    @field_validator("create_item_part_number",
                     "consume_item_part_number", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value