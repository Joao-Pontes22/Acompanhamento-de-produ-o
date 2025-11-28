from pydantic import BaseModel



class Components_Scheme(BaseModel):
    part_number : str
    description_material : str
    supplier_ID : int
    cost : float
    class Config:
        from_attributes = True
    
class Components_Scheme_Update(BaseModel):
    part_number : str | None = None
    description_material : str | None = None
    supplier_ID : int | None = None
    cost : float | None = None
    class Config:
        from_attributes = True

class Parts_Scheme(BaseModel):
    part_number: str
    description_parts: str
    clients_ID: int
    cost: float
    class Config:
        from_attributes = True

class parts_Update_Scheme(BaseModel):
    part_number: str | None = None
    description_parts: str | None = None
    clients_ID: int | None = None
    cost: float | None = None
    class Config:
        from_attributes = True

class Clients_Scheme(BaseModel):
    name: str
    contact: str
    email: str
    phone: str
    class Config:
        from_attributes = True

class Clients_Update_Scheme(BaseModel):
    name: str |  None = None
    contact: str | None = None
    email: str | None = None
    phone: str | None = None
    class Config:
        from_attributes = True