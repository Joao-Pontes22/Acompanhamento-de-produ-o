from pydantic import BaseModel



class Suppliers_Scheme(BaseModel):
    name : str
    contact : str
    email : str
    phone : str

    class Config:
        from_attributes = True

class Suppliers_Scheme_Update(BaseModel):
    name : str = None
    contact : str = None
    email : str = None
    phone : str = None
    
    class Config:
        from_attributes = True