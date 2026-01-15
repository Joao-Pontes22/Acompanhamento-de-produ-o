from pydantic import BaseModel, ConfigDict
from datetime import date

class Response_Stock_Scheme(BaseModel):
    ID: int
    sector_name: str
    part_number: str
    batch: str | None = None
    machining_batch: str | None = None
    machining_date: date | None = None
    assembly_batch: str | None = None
    assembly_date: date | None = None
    qnty: int
    entry_date: date | None = None
    supplier_name: str | None = None
    status: str
    cost: float
    client_name: str | None = None

    model_config = ConfigDict(from_attributes=True)