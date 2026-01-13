from pydantic import BaseModel, ConfigDict

class Parts_Scheme(BaseModel):
    part_number: str
    description: str
    client: str
    cost: float
    model_config = ConfigDict(from_attributes=True)

class parts_Update_Scheme(BaseModel):
    part_number: str | None = None
    description: str | None = None
    client: str | None = None
    cost: float | None = None
    model_config = ConfigDict(from_attributes=True)

