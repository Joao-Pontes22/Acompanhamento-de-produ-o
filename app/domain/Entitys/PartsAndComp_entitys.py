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

# Entity for filtering parts and components
class PartsAndCompsEntityFilter:
    def __init__(self, 
                 part_number: str, 
                 description: str, 
                 supplier: str, 
                 client: str, 
                 component_type: str
                 ):
        
        if part_number:
            self.part_number = part_number

        if description:
            self.description = description 

        if supplier:
            self.supplier = supplier

        if client:
            self.client = client

        if component_type:
            self.component_type = component_type
      