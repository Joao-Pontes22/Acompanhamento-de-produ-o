from app.Schemes.Stock_Schemes import Stock_Scheme
# Entity for creating a new stock record

class StockEntity:
    def __init__(self,
                 sector_name: str,
                 part_number: str,
                 qnty: int,
                 reason: str, 
                 cost:float):
        
        self.sector_name = sector_name
        self.part_number = part_number
        self.qnty = qnty
        self.reason = reason
        self.cost = qnty * cost
        self._validate_business_rules()

    def _validate_business_rules(self):
        if self.qnty <= 0:
            raise ValueError("Stock quantity must be greater than zero")
# Entity for creating stock records based on part type
class StockEntityPart:
    def __init__(self, 
                 sector_name: str,
                 part_number: str ,
                 qnty: int,
                 reason:str,
                 cost: float,  
                 client:str,  
                 assembly_batch:str,
                 assembly_date:str
                 ):
        
        self.sector_name = sector_name
        self.part_number = part_number
        self.qnty = qnty
        self.reason = reason
        self.assembly_batch = assembly_batch
        self.assembly_date = assembly_date 
        self.machining_batch =  None
        self.machining_date = None
        self.batch =  None
        self.cost = cost
        self.client_name = client.upper() 
        self.entry_date = None
        self.supplier_name = None
        self._validate_business_rules()

    def _validate_business_rules(self):
        if self.qnty <= 0:
            raise ValueError("Stock quantity must be greater than zero")
# Entity for creating stock records for machined parts
class StockEntityMachined:
    def __init__(self,
                 sector_name: str,
                 part_number: str,
                 qnty: int,
                 reason: str,
                 cost: float,
                supplier:str,  
                 machining_batch: str,
                 machining_date):
        
        self.sector_name = sector_name
        self.part_number = part_number
        self.qnty = qnty
        self.reason = reason
        self.assembly_batch = None
        self.assembly_date = None
        self.machining_batch =  machining_batch
        self.machining_date = machining_date
        self.batch =  None
        self.cost = cost
        self.client_name = None
        self.entry_date = None
        self.supplier_name = supplier
        self._validate_business_rules()

    def _validate_business_rules(self):
        if self.qnty <= 0:
            raise ValueError("Stock quantity must be greater than zero")
# Entity for creating stock records for raw materials
class StockEntityRaw:
    def __init__(self,
                 sector_name: str,
                 part_number: str,
                 qnty: int,
                 reason: str,
                 cost: float, 
                  supplier:str,  
                 batch: str,
                 entry_date):
        
        self.sector_name = sector_name
        self.part_number = part_number
        self.qnty = qnty
        self.reason = reason
        self.assembly_batch = None
        self.assembly_date = None
        self.machining_batch =  None
        self.machining_date = None
        self.batch =  batch
        self.cost = cost
        self.client_name = None
        self.entry_date = entry_date
        self.supplier_name = supplier
        self._validate_business_rules()

    def _validate_business_rules(self):
        if self.qnty <= 0:
            raise ValueError("Stock quantity must be greater than zero")
        