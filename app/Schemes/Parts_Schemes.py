from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class PartsScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    part_number: str
    description: str
    client: str
    cost: float
    
    @field_validator("part_number",
                     "description", 
                     "client", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

class UpdatePartsInfoScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    part_number: Optional[str] 
    description: Optional[str] 
    client: Optional[str] 
    cost: Optional[float] 

    @field_validator("part_number",
                     "description", 
                     "client", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
