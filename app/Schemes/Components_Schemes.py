from pydantic import BaseModel, ConfigDict


class Components_Scheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    part_number : str
    description : str
    supplier_ID : int
    cost : float

    
class Components_Scheme_Update(BaseModel):
    part_number : str | None = None
    description : str | None = None
    supplier_ID : int | None = None
    cost : float | None = None
    model_config = ConfigDict(from_attributes=True)
