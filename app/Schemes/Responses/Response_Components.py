from pydantic import BaseModel, ConfigDict



class Responde_Components(BaseModel):
    id: int
    part_number: str
    description: str
    cost: float
    model_config = ConfigDict(from_attributes=True)