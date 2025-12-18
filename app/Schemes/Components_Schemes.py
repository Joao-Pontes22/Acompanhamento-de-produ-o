from pydantic import BaseModel


class Components_Scheme(BaseModel):
    part_number : str
    description : str
    supplier_ID : int
    cost : float
    class Config:
        from_attributes = True
    
class Components_Scheme_Update(BaseModel):
    part_number : str | None = None
    description : str | None = None
    supplier_ID : int | None = None
    cost : float | None = None
    class Config:
        from_attributes = True
