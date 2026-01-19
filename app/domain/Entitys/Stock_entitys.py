from app.Schemes.Stock_Schemes import Stock_Scheme
# Entity for creating a new stock record
class Stock_Entity:
    def __init__(self, scheme: Stock_Scheme, 
                 cost:float):
        
        self.sector = scheme.sector.upper()
        self.part_number = scheme.part_number.upper()
        self.qnty = scheme.qnty
        self.reason = scheme.reason.upper()
        self.cost = scheme.qnty * cost
        self._validate_business_rules()

    def _validate_business_rules(self):
        if self.qnty <= 0:
            raise ValueError("Stock quantity must be greater than zero")
# Entity for creating stock records based on part type
class Stock_Entity_Part:
    def __init__(self, scheme: Stock_Entity,  client:str,  
                 assembly_batch:str = None,
                 assembly_date:str = None):
        
        self.sector_name = scheme.sector.upper()
        self.part_number = scheme.part_number.upper()
        self.qnty = scheme.qnty
        self.reason = scheme.reason.upper()
        self.assembly_batch = assembly_batch.upper() 
        self.assembly_date = assembly_date 
        self.machining_batch =  None
        self.machining_date = None
        self.batch =  None
        self.cost = scheme.cost
        self.client_name = client.upper() 
        self.entry_date = None
        self.supplier_name = None
        self._validate_business_rules()

    def _validate_business_rules(self):
        if self.qnty <= 0:
            raise ValueError("Stock quantity must be greater than zero")
# Entity for creating stock records for machined parts
class Stock_Entity_Machined:
    def __init__(self, scheme: Stock_Entity,
                supplier:str,  
                 machining_batch: str,
                 machining_date):
        
        self.sector_name = scheme.sector.upper()
        self.part_number = scheme.part_number.upper()
        self.qnty = scheme.qnty
        self.reason = scheme.reason.upper()
        self.assembly_batch = None
        self.assembly_date = None
        self.machining_batch =  machining_batch
        self.machining_date = machining_date
        self.batch =  None
        self.cost = scheme.cost
        self.client_name = None
        self.entry_date = None
        self.supplier_name = supplier
        self._validate_business_rules()

    def _validate_business_rules(self):
        if self.qnty <= 0:
            raise ValueError("Stock quantity must be greater than zero")
# Entity for creating stock records for raw materials
class Stock_Entity_Raw:
    def __init__(self, scheme: Stock_Entity, 
                  supplier:str,  
                 batch: str,
                 entry_date):
        
        self.sector_name = scheme.sector.upper()
        self.part_number = scheme.part_number.upper()
        self.qnty = scheme.qnty
        self.reason = scheme.reason.upper()
        self.assembly_batch = None
        self.assembly_date = None
        self.machining_batch =  None
        self.machining_date = None
        self.batch =  batch
        self.cost = scheme.cost
        self.client_name = None
        self.entry_date = entry_date
        self.supplier_name = supplier
        self._validate_business_rules()

    def _validate_business_rules(self):
        if self.qnty <= 0:
            raise ValueError("Stock quantity must be greater than zero")
        