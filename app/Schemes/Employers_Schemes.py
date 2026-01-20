from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class EmployersScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    emp_id: str
    password: str
    sector_name: str

    @field_validator("name",
                     "emp_id", 
                     "sector_name", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    

    
class UpdateEmployersInfoScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] 
    sector_name: Optional[str]
    password: Optional[str]
    emp_id: Optional[str]

    @field_validator("name",
                     "emp_id", 
                     "sector_name", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    