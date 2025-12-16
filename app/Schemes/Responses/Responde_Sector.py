from pydantic import BaseModel

class Response_Sector(BaseModel):
    ID: int
    sector: str
    tag: str

    class Config:
        from_attributes = True