from pydantic import BaseModel



class Responde_Components(BaseModel):
    id: int
    part_number: str
    description: str
    cost: float
    class Config:
        from_attributes = True