from pydantic import BaseModel



class Responde_Parts(BaseModel):
    id: int = None
    part_number: str = None
    description: str = None
    client_ID: int = None
    cost: float = None
    class Config:
        from_attributes = True