from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date
from typing import Optional


class MachiningProductionScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sector_name : str
    machine_name : str
    Date : date
    duration_process : int
    input_part_number : str
    output_part_number : str
    batch : str
    emp_id : str
    status : str

    @field_validator("machine_name", 
                     "sector_name", 
                     "input_part_number",
                     "output_part_number",
                     "batch",
                     "emp_id", 
                     mode="before"
                     )
    @classmethod


    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    

class MachiningProductionfilteredScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sector_name : Optional[str]
    machine_name : Optional[str]
    Date : Optional[date]
    input_part_number : Optional[str]
    output_part_number : Optional[str]
    machining_batch : Optional[str] 
    batch : Optional[str] 
    emp_id : Optional[str]
    status : Optional[str]

    @field_validator("machine_name", 
                     "sector_name", 
                     "input_part_number",
                     "output_part_number",
                     "batch",
                     "emp_id", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    