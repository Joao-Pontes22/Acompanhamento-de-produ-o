from pydantic import BaseModel, ConfigDict


class Warehouse_Scehem(BaseModel):
    sector_ID : int
    part_number : str
    warehouse_batch : str
    qnty : int
    entry_date_warehouse_batch : str
    supplier_ID : int
    status : str
    cost : str
    model_config = ConfigDict(from_attributes=True)
