from datetime import date
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

class StockScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sector_name: str
    part_number: str
    qnty: int
    reason:str

    @field_validator("sector_name",
                     "part_number",
                     "reason", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    




class StockSchemeModels(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sector_name: str
    part_number: str
    qnty: int
    cost: float
    batch: Optional[str] 
    machining_batch: Optional[str] 
    machining_date: Optional[date] 
    assembly_batch: Optional[str] 
    assembly_date: Optional[date] 
    entry_date: Optional[date] 
    supplier_name: Optional[str] 
    client_name: Optional[str] 

    @field_validator("sector_name",
                     "part_number",
                     "batch",
                     "machining_batch",
                      "assembly_batch",
                      "supplier_name",
                      "client_name",
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    



class UpdateStockInfoScheme(BaseModel):
    sector_name: str = None
    part_number: str = None
    qnty: int = None
    reason:str = None
    model_config = ConfigDict(from_attributes=True)

    @field_validator("sector_name",
                     "part_number",
                     "reason", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

class StockTransferScheme(BaseModel):
    part_number: str
    origin_sector: str
    destination_sector: str
    qnty: int
    batch: Optional[str] 
    machining_batch : Optional[str] 
    assembly_batch: Optional[str] 
    reason: str
    model_config = ConfigDict(from_attributes=True)

    @field_validator("origin_sector",
                     "part_number",
                     "batch",
                     "machining_batch",
                      "assembly_batch",
                      "destination_sector",
                      "reason",
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value