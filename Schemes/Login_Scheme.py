from pydantic import BaseModel

class Login_Scheme(BaseModel):
    name: str
    password: str
    class Config:
        from_attributes = True