class Relation_Entity:
    def __init__(self, create_item_part_number: str, consume_item_part_number: str, qnty: int):
        self.create_item_part_number = create_item_part_number.upper()
        self.consume_item_part_number = consume_item_part_number.upper()
        self.qnty = qnty


class Relation_Entity_filtred:
    def __init__(self, id: int | None = None, create_item_part_number: str | None = None, consume_item_part_number: str | None = None):
        self.id = id
        self.create_item_part_number = create_item_part_number.upper() if create_item_part_number else None
        self.consume_item_part_number = consume_item_part_number.upper() if consume_item_part_number else None