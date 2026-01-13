from pydantic import BaseModel, ConfigDict


class Components_Scheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    part_number : str
    description : str
    supplier : str
    cost : float
    component_type: str

    
class Components_Scheme_Update(BaseModel):
    part_number : str | None = None
    description : str | None = None
    supplier : str | None = None
    cost : float | None = None
    component_type: str | None = None
    model_config = ConfigDict(from_attributes=True)
