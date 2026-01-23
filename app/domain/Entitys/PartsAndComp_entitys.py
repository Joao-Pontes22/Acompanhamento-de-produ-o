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

