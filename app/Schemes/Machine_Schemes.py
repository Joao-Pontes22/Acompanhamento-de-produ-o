from pydantic import BaseModel




class Machine_Scheme(BaseModel):
    machine: str
    sector_ID: int
    description_machine: str
    class config():
        from_attributes = True
        
class Update_Machine_Scheme(BaseModel):
    machine: str = None
    sector_ID: int = None
    description_machine: str = None
    class config():
        from_attributes = True