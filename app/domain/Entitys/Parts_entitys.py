from typing import Optional
# Entity for creating or updating a part
class PartsEntity: 
    def __init__(self,
                 part_number: str,
                 description: str,
                 cost: float,
                 client_name: str
                 ):
            
            self.part_number = part_number
            self.description_parts = description
            self.cost = cost
            self.client = client_name
    
    def validate_rules(self):
        if self.cost <=0:
             raise ValueError("Cost must be greater than zero")
        
class UpdatePartsInfoEntity: 
    def __init__(self,
                 part_number: Optional[str] = None,
                 description: Optional[str] = None,
                 cost: Optional[float] = None,
                 client_name: Optional[str] = None
                 ):
        
        if part_number:
            self.part_number = part_number
        if description:
            self.description_parts = description
        if cost:
            self.cost = cost
        if client_name:
            self.client = client_name