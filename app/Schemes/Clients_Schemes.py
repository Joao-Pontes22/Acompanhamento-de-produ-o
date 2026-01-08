from pydantic import BaseModel, ConfigDict

class Clients_Scheme(BaseModel):
    name: str
    contact: str
    email: str
    phone: str

    model_config = ConfigDict(from_attributes=True)


class Clients_Update_Scheme(BaseModel):
    name: str |  None = None
    contact: str | None = None
    email: str | None = None
    phone: str | None = None
    
    model_config = ConfigDict(from_attributes=True)