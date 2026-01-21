from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class MovimentationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    part_number: str
    sector_origin: str
    reason: str
    movimentation_type: str
    emp_id: str
    batch: Optional[str] 
    qnty: int
    date: str
    sector_destination: str
    machining_batch: Optional[str] 
    assembly_batch: Optional[str]

    @field_validator("part_number", 
                     "sector_origin", 
                     "reason",
                     "movimentation_type",
                     "emp_id",
                     "batch",
                     "emp_id",
                     "sector_destination",
                     "machining_batch",
                     "assembly_batch", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value  
    