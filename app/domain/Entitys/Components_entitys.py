from typing import Optional

# Entity for creating or updating a component
class ComponentsEntity: 
    def __init__(self,
                 part_number: str,
                 description_material: str,
                 cost: float,
                 supplier_name: str,
                 component_type: str
                 ):
            
            self.part_number = part_number
            self.description_material = description_material
            self.cost = cost
            self.supplier_name = supplier_name
            self.component_type = component_type
            self._validation_rules()

    def _validation_rules(self):
        if self.cost <=0:
                raise ValueError("Cost must be greater than zero")

class UpdateComponentsInfoEntity: 
    def __init__(self,
                 part_number: Optional[str] = None,
                 description_material: Optional[str] = None,
                 cost: Optional[float] = None,
                 supplier_name: Optional[str] = None,
                 component_type: Optional[str] = None
                 ):

        if part_number:
            self.part_number = part_number

        if description_material:
            self.description_material = description_material

        if cost:
            self.cost = cost

        if supplier_name:
            self.supplier_name = supplier_name

        if component_type:
            self.component_type = component_type

        self._validation_rules()

    def _validation_rules(self):
        if self.cost <=0:
                raise ValueError("Cost must be greater than zero")