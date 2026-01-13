from pydantic import BaseModel, ConfigDict

class Response_Machines(BaseModel):
    ID: int
    machine: str
    sector_name: str
    description_machine: str
    model_config = ConfigDict(from_attributes=True)