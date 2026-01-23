from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date

class MovimentationParameters(BaseModel):
    movimentation_id: Optional[int] = None
    part_number: Optional[str] = None
    batch: Optional[str] = None 
    start_date: Optional[date] = None 
    end_date: Optional[date] = None 
    emp_id: Optional[int] = None
    movimentation_type: Optional[str] = None
    sector_origin: Optional[str] = None
    sector_destination: Optional[str] = None
    machining_batch: Optional[str] = None
    assembly_batch: Optional[str] = None


    @field_validator("part_number",
                     "batch",
                     "emp_id",
                     "movimentation_type",
                     "sector_origin",
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




                                    