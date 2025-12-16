from pydantic import BaseModel

class Parts_Scheme(BaseModel):
    part_number: str
    description_parts: str
    clients_ID: int
    cost: float
    class Config:
        from_attributes = True

class parts_Update_Scheme(BaseModel):
    part_number: str | None = None
    description_parts: str | None = None
    clients_ID: int | None = None
    cost: float | None = None
    class Config:
        from_attributes = True

