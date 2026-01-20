# Entity for creating or updating relation between items
class RelationsEntity:
    def __init__(self, 
                 create_item_part_number: str, 
                 consume_item_part_number: str, 
                 qnty: int
                 ):
        
        self.create_item_part_number = create_item_part_number
        self.consume_item_part_number = consume_item_part_number
        self.qnty = qnty

# Entity for filtering relations between items
class RelationsEntityFiltred:
    def __init__(self, 
                 id: int, 
                 create_item_part_number: str, 
                 consume_item_part_number: str
                 ):
        
        self.id = id

        if create_item_part_number:
            self.create_item_part_number = create_item_part_number.upper() 

        if consume_item_part_number:
            self.consume_item_part_number = consume_item_part_number.upper() 