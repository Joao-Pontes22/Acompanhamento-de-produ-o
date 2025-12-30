from app.Schemes.Stock_Schemes import Stock_Scheme_Part, Update_Part_Stock_Scheme, Update_Machined_Stock_Scheme, Update_Raw_Stock_Scheme
from app.Schemes.Stock_Schemes import Stock_Scheme_machined_Coponent, Stock_Scheme_Raw_Coponent
from  fastapi import HTTPException
class Stock_Entity_Parts:
    def __init__(self, scheme: Stock_Scheme_Part, cost:float, client_id:int):
        self.sector_id = scheme.sector_ID
        self.part_number = scheme.part_number.upper()
        self.qnty = scheme.qnty
        self.status = scheme.status.upper()
        self.assembly_batch = scheme.assembly_batch
        self.assembly_date = scheme.assembly_date
        self.cost = scheme.qnty * cost
        self.client_id = client_id
        self._validate_business_rules()

    def _validate_business_rules(self):
        if self.qnty <= 0:
            raise ValueError("Stock quantity must be greater than zero")

        if self.status not in {"ACTIVE", "INACTIVE", "BLOCKED"}:
            raise HTTPException(status_code=400, detail="Invalid stock status")

class Stock_Entity_machined_Component:
    def __init__(self, scheme:Stock_Scheme_machined_Coponent, cost:float, supplier_id:int):
        self.sector_ID = scheme.sector_ID
        self.part_number = scheme.part_number
        self.qnty = scheme.qnty
        self.status = scheme.status.upper()
        self.machining_batch = scheme.machining_batch
        self.machining_date = scheme.machining_date
        self.cost = scheme.qnty * cost
        self.supplier_id =  supplier_id
        pass

class Stock_Entity_Raw_Component:
    def __init__(self, scheme:Stock_Scheme_Raw_Coponent, cost:float, supplier_id:int):
        self.sector_ID = scheme.sector_ID
        self.part_number = scheme.part_number
        self.qnty = scheme.qnty
        self.status = scheme.status.upper()
        self.entry_date = scheme.entry_date
        self.batch = scheme.batch
        self.cost = scheme.qnty * cost
        self.supplier_id =  supplier_id
        pass


class Updated_Part_Stock_Entity:
    def __init__(self, scheme:Update_Part_Stock_Scheme):
        if scheme.sector_ID is not None:
            self.sector_ID = scheme.sector_ID
        if scheme.part_number is not None:
            self.part_number = scheme.part_number
        if scheme.qnty is not None:
            self.qnty = scheme.qnty
        if scheme.status is not None:
            self.status = scheme.status
        if scheme.assembly_batch is not None:
            self.assembly_batch = scheme.assembly_batch
        if scheme.assembly_date is not None:
            self.assembly_date = scheme.assembly_date
        