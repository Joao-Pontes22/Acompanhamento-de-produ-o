from pydantic import BaseModel, ConfigDict



class ResponseComponents(BaseModel):
    id: int
    part_number: str
    description: str
    cost: float
    supplier_name: str
    component_type: str
    model_config = ConfigDict(from_attributes=True)