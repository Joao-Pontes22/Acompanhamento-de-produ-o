from pydantic import BaseModel, ConfigDict



class Responde_Parts(BaseModel):
    id: int = None
    part_number: str = None
    description: str = None
    client_ID: int = None
    cost: float = None
    model_config = ConfigDict(from_attributes=True)