
class PartsAndComp_entity:
    def __init__(self, part_number, description, category, cost):
        self.part_number = part_number
        self.description = description
        self.category = category.upper()
        self.cost = cost
        pass