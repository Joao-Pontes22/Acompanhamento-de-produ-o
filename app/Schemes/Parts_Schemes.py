from pydantic import BaseModel, ConfigDict

class Parts_Scheme(BaseModel):
    part_number: str
    description: str
    client_ID: int
    cost: float
    model_config = ConfigDict(from_attributes=True)

class parts_Update_Scheme(BaseModel):
    part_number: str | None = None
    description: str | None = None
    client_ID: int | None = None
    cost: float | None = None
    model_config = ConfigDict(from_attributes=True)

