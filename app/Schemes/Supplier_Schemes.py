from pydantic import BaseModel, ConfigDict



class Suppliers_Scheme(BaseModel):
    name : str
    contact : str
    email : str
    phone : str
    model_config = ConfigDict(from_attributes=True)

class Suppliers_Scheme_Update(BaseModel):
    name : str = None
    contact : str = None
    email : str = None
    phone : str = None
    model_config = ConfigDict(from_attributes=True)