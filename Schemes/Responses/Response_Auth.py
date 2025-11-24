from pydantic import BaseModel

class Response_Auth(BaseModel):
    ID: int
    name: str
    sector_name: str
    sector_tag : str
    
    class Config:
        from_attributes = True