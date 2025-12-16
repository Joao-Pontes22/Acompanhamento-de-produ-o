from pydantic import BaseModel
from typing import Optional
class Employers_Scheme(BaseModel):
    name: str
    password: str
    sector_ID: int
    class Config:
        from_attributes = True

class Employers_Scheme_Update(BaseModel):
    name: Optional[str] = None
    sector_ID: Optional[int] = None
    class Config:
        from_attributes = True