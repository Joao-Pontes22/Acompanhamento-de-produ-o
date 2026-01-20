from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class MachineScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    machine: str
    sector_name: str
    description_machine: str

    @field_validator("machine", 
                     "sector_name", 
                     "description_machine", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    
    


class UpdateMachineInfoScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    machine: Optional[str] 
    sector_name: Optional[str] 
    description_machine: Optional[str] 

    @field_validator("machine", 
                     "sector_name", 
                     "description_machine", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    