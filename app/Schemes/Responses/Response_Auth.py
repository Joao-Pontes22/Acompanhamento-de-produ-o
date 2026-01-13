from pydantic import BaseModel, ConfigDict

class Response_Auth(BaseModel):
    ID: int
    name: str
    sector_name: str
    emp_id: str
    model_config = ConfigDict(from_attributes=True)