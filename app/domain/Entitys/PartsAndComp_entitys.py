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
                 part_number: str = None, 
                 description: str = None, 
                 supplier: str = None, 
                 client: str = None, 
                 component_type: str = None
                 ):
        
        if part_number:
            self.part_number = part_number.upper()

        if description:
            self.description = description.upper() 

        if supplier:
            self.supplier = supplier.upper()

        if client:
            self.client = client.upper()

        if component_type:
            self.component_type = component_type.upper()
      