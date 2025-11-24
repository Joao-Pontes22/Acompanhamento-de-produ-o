from pydantic import BaseModel



class Suppliers_Scheme(BaseModel):
    supplier_name : str
    contact_name : str
    contact_email : str
    contact_phone : str

    class Config:
        from_attributes = True

class Suppliers_Scheme_Update(BaseModel):
    supplier_name : str | None = None
    contact_name : str | None = None
    contact_email : str | None = None
    contact_phone : str | None = None
    
    class Config:
        from_attributes = True