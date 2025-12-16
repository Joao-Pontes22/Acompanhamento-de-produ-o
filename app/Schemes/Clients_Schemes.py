from pydantic import BaseModel

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