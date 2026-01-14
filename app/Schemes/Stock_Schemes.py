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
    sector_name: int
    part_number: str
    qnty: int
    cost: float
    batch: str | None = None
    machining_batch: str | None = None
    machining_date: date | None = None
    assembly_batch: str | None = None
    assembly_date: date | None = None
    entry_date: date | None = None
    supplier_ID: int | None = None
    client_ID: int | None = None

    model_config = ConfigDict(from_attributes=True)



class Update_Part_Stock_Scheme(BaseModel):
    sector_ID: int | None = None
    part_number: str | None = None
    qnty: int | None = None
    status: str | None = None
    assembly_batch:str | None = None
    assembly_date:date | None = None
    reason:str | None = None
    model_config = ConfigDict(from_attributes=True)

class Update_Raw_Stock_Scheme(BaseModel):
    sector_ID: int | None = None
    part_number: str | None = None
    qnty: int | None = None
    batch : str | None = None
    status: str | None = None
    entry_date : date | None = None
    reason:str | None = None
    model_config = ConfigDict(from_attributes=True)

class Update_Machined_Stock_Scheme(BaseModel):
    sector_ID : int | None = None
    part_number : str | None = None
    machining_batch : str | None = None
    machining_date : date | None = None
    qnty : int | None = None
    status : str | None = None
    reason:str | None = None
    model_config = ConfigDict(from_attributes=True)



class Stock_Transfer_Scheme(BaseModel):
    part_number: str
    origin_sector_id: int
    destination_sector_id: int
    qnty: int
    batch: str | None = None
    machining_batch : str | None = None
    assembly_batch: str | None = None
    reason: str
    model_config = ConfigDict(from_attributes=True)