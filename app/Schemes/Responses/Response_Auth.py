from pydantic import BaseModel, ConfigDict

class Response_Auth(BaseModel):
    ID: int
    name: str
    sector_ID: int
    emp_id: str
    model_config = ConfigDict(from_attributes=True)