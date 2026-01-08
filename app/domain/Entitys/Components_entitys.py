from app.Schemes.Components_Schemes import Components_Scheme

class Components_entity: 
    def __init__(self,scheme:Components_Scheme):
        if scheme.part_number is not None:
            self.part_number = scheme.part_number.upper()
        if scheme.description is not None:
            self.description_material = scheme.description.upper()
        if scheme.cost is not None:
            if scheme.cost <=0:
                raise ValueError("Cost must be greater than zero")
            self.cost = scheme.cost
        if scheme.supplier_ID is not None:
            self.supplier_ID = scheme.supplier_ID