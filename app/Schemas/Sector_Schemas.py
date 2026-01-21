from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

class SectorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sector_name: str
    tag: str

    @field_validator("sector_name",
                     "tag", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    

class UpdateSectorInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sector_name: Optional[str] 
    tag: Optional[str]

    @field_validator("sector_name",
                     "tag", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    