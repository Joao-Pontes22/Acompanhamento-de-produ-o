from app.Schemes.Parts_Schemes import Parts_Scheme

class Parts_entity: 
    def __init__(self,scheme:Parts_Scheme):
        if scheme.part_number is not None:
            self.part_number = scheme.part_number.upper()
        if scheme.description is not None:
            self.description_parts = scheme.description.upper()
        if scheme.cost is not None:
            self.cost = scheme.cost
        if scheme.client_ID is not None:
            self.client_ID = scheme.client_ID