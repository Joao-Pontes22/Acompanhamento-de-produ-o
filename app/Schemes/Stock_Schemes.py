from datetime import date
from pydantic import BaseModel


class Stock_Scheme_warehouse(BaseModel):
    sector_ID: int
    part_number: str
    qnty: int
    entry_date_warehouse_batch: date
    supplier_ID: int