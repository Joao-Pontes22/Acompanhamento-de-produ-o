from pydantic import BaseModel
from typing import Optional

class Sector_Scheme_Update(BaseModel):
    sector: Optional[str] = None
    tag: Optional[str] = None

    class Config:
        from_attributes = True

class Sector_Scheme(BaseModel):
    sector: str
    tag: str

    class Config:
        from_attributes = True