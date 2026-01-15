from app.Schemes.Stock_Schemes import Stock_Scheme, Update_Stock_Scheme

class Stock_Entity:
    def __init__(self, scheme: Stock_Scheme, 
                 cost:float, client:str, 
                 batch:str = None, 
                 machining_batch:str = None, 
                 assembly_batch:str = None,
                 assembly_date:str = None,
                 machining_date:str = None,
                 entry_date:str = None,
                 supplier:str = None):
        
        self.sector = scheme.sector.upper()
        self.part_number = scheme.part_number.upper()
        self.qnty = scheme.qnty
        self.reason = scheme.reason.upper()
        self.assembly_batch = assembly_batch.upper() if assembly_batch else None
        self.assembly_date = assembly_date if assembly_date else None
        self.machining_batch = machining_batch.upper() if machining_batch else None
        self.machining_date = machining_date if machining_date else None
        self.batch = batch.upper() if batch else None
        self.cost = scheme.qnty * cost
        self.client_name = client.upper() if client else None
        self.entry_date = entry_date if entry_date else None
        self.supplier_name = supplier.upper() if supplier else None
        self._validate_business_rules()

    def _validate_business_rules(self):
        if self.qnty <= 0:
            raise ValueError("Stock quantity must be greater than zero")

        