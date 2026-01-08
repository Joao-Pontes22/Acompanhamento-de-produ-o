from pydantic import BaseModel, ConfigDict
from typing import Optional
class Employers_Scheme(BaseModel):
    name: str
    emp_id: str
    password: str
    sector_ID: int
    model_config = ConfigDict(from_attributes=True)

class Employers_Scheme_Update(BaseModel):
    name: Optional[str] = None
    sector_ID: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)