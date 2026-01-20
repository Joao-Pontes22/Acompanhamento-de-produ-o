from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class ComponentsScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    part_number : str
    description : str
    supplier_name : str
    cost : float
    component_type: str

    @field_validator("part_number",
                     "description", 
                     "supplier_name", 
                     "component_type", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

class UpdateComponentsInfoScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    part_number : Optional[str] 
    description : Optional[str] 
    supplier_name : Optional[str]
    cost : Optional[float]
    component_type: Optional[str]

    @field_validator("part_number",
                     "description", 
                     "supplier_name", 
                     "component_type", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    
