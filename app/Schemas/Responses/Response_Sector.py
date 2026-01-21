from pydantic import BaseModel, ConfigDict

class ResponseSector(BaseModel):
    ID: int
    sector: str
    tag: str
    model_config = ConfigDict(from_attributes=True)