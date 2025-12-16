from pydantic import BaseModel

class Login_Scheme(BaseModel):
    id: int
    password: str
    class Config:
        from_attributes = True