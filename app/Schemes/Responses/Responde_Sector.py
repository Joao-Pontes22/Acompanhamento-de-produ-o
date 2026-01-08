from pydantic import BaseModel, ConfigDict

class Response_Sector(BaseModel):
    ID: int
    sector: str
    tag: str
    model_config = ConfigDict(from_attributes=True)