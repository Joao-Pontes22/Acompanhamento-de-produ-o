from datetime import date
from pydantic import BaseModel, ConfigDict
from typing import Optional

class Stock_Scheme(BaseModel):
    sector: str
    part_number: str
    qnty: int
    reason:str
    model_config = ConfigDict(from_attributes=True)




class Stock_Scheme_models(BaseModel):
    sector_name: str
    part_number: str
    qnty: int
    cost: float
    batch: str | None = None
    machining_batch: str | None = None
    machining_date: date | None = None
    assembly_batch: str | None = None
    assembly_date: date | None = None
    entry_date: date | None = None
    supplier_name: str | None = None
    client_name: str | None = None

    model_config = ConfigDict(from_attributes=True)



class Update_Stock_Scheme(BaseModel):
    sector: str = None
    part_number: str = None
    qnty: int = None
    reason:str = None
    model_config = ConfigDict(from_attributes=True)


class Stock_Transfer_Scheme(BaseModel):
    part_number: str
    origin_sector: str
    destination_sector: str
    qnty: int
    batch: str | None = None
    machining_batch : str | None = None
    assembly_batch: str | None = None
    reason: str
    model_config = ConfigDict(from_attributes=True)