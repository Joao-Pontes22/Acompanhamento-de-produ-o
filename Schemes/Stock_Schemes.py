from pydantic import BaseModel


class Stock_Scheme_warehouse(BaseModel):
    sector_ID: int
    part_number: str
    warehouse_batch: str
    machining_batch: str = None
    machining_date: str = None
    qnty: int
    entry_date_warehouse_batch: str
    supplier_ID: int
    status: str
    cost: str