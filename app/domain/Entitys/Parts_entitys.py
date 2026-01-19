from app.Schemes.Parts_Schemes import Parts_Scheme
# Entity for creating or updating a part
class Parts_entity: 
    def __init__(self,scheme:Parts_Scheme):
        if scheme.part_number is not None:
            self.part_number = scheme.part_number.upper()
        if scheme.description is not None:
            self.description_parts = scheme.description.upper()
        if scheme.cost is not None:
            if scheme.cost <=0:
             raise ValueError("Cost must be greater than zero")
            self.cost = scheme.cost
        if scheme.client is not None:
            self.client = scheme.client.upper()