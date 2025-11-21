from pydantic import BaseModel

class Auth_Scheme(BaseModel):
    name: str
    password: str
    sector_ID: int
    class Config:
        from_attributes = True