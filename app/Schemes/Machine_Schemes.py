from pydantic import BaseModel, ConfigDict




class Machine_Scheme(BaseModel):
    machine: str
    sector: str
    description_machine: str
    model_config = ConfigDict(from_attributes=True)
        
class Update_Machine_Scheme(BaseModel):
    machine: str = None
    sector: str = None
    description_machine: str = None
    model_config = ConfigDict(from_attributes=True)