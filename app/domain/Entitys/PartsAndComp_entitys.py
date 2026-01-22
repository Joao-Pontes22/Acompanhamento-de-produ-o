from typing import Optional

# Entity for creating or updating parts and components
class PartsAndCompsEntity:
    def __init__(self, 
                 part_number: str, 
                 description: str, 
                 category: str, 
                 cost: float
                 ):
        
        self.part_number = part_number
        self.description = description
        self.category = category
        self.cost = cost


class UpdatePartsEntity:
    def __init__(self):
        pass
# Entity for filtering parts and components
class PartsAndCompsEntityFilter:
    def __init__(self, 
                 part_number: Optional[str] = None, 
                 description: Optional[str] = None, 
                 supplier: Optional[str] = None, 
                 client: Optional[str] = None, 
                 component_type: Optional[str] = None
                 ):
        
        
        self.part_number = part_number.upper() if part_number else None

        
        self.description = description.upper() if description else None

        
        self.supplier = supplier.upper() if supplier else None

        
        self.client = client.upper() if client else None

        
        self.component_type = component_type.upper() if component_type else None
      