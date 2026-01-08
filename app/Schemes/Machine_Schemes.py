from pydantic import BaseModel, ConfigDict




class Machine_Scheme(BaseModel):
    machine: str
    sector_ID: int
    description_machine: str
    model_config = ConfigDict(from_attributes=True)
        
class Update_Machine_Scheme(BaseModel):
    machine: str = None
    sector_ID: int = None
    description_machine: str = None
    model_config = ConfigDict(from_attributes=True)