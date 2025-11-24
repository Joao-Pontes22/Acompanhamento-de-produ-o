from pydantic import BaseModel


class Warehouse_Scehem(BaseModel):
    sector_ID : int
    part_number : str
    warehouse_batch : str
    machining_date : str
    qnty : int
    entry_date_warehouse_batch : str
    supplier_ID : int
    status : str
    cust : str

