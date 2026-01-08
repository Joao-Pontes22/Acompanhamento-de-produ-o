from pydantic import BaseModel, ConfigDict
from typing import Optional

class Sector_Scheme_Update(BaseModel):
    sector: Optional[str] = None
    tag: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class Sector_Scheme(BaseModel):
    sector: str
    tag: str
    model_config = ConfigDict(from_attributes=True)