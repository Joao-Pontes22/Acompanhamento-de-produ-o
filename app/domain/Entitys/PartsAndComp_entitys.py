# Entity for creating or updating parts and components
class PartsAndComp_entity:
    def __init__(self, part_number, description, category, cost):
        self.part_number = part_number
        self.description = description
        self.category = category.upper()
        self.cost = cost
        pass

# Entity for filtering parts and components
class PartsAndComp_entity_filter:
    def __init__(self, part_number=None, description=None, supplier=None, client=None, component_type=None):
        self.part_number = part_number.upper() if part_number else None
        self.description = description.upper() if description else None
        self.supplier = supplier.upper() if supplier else None
        self.client = client.upper() if client else None
        self.component_type = component_type.upper() if component_type else None
        pass