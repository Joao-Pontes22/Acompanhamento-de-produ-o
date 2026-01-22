from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class ComponentsSchema(BaseModel):
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

class UpdateComponentsInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    part_number : Optional[str] = None
    description : Optional[str] = None
    supplier_name : Optional[str] = None
    cost : Optional[float] = None
    component_type: Optional[str] = None

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
    
