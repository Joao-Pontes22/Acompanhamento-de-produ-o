from pydantic import BaseModel, field_validator
from typing import Optional


class StockParameters(BaseModel):

    part_number: Optional[str] = None
    status: Optional[str] = None
    sector_name: Optional[str] = None
    batch: Optional[str] = None
    machining_batch: Optional[str] = None
    assembly_batch: Optional[str] = None

    @field_validator("part_number",
                     "status",
                     "sector_name", 
                     "batch",
                     "machining_batch", 
                     "assembly_batch", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value