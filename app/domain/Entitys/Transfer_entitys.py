class Transfer_entitys:
    def __init__(self, 
                 part_number: str,
                 origin_sector_id: int,
                 destination_sector_id: int,
                 qnty: int,
                 reason: str,
                 batch: str = None,
                 machining_batch: str = None,
                 assembly_batch: str = None):
        self.part_number = part_number
        self.origin_sector_id = origin_sector_id
        self.destination_sector_id = destination_sector_id
        self.qnty = qnty
        self.reason = reason
        self.batch = batch
        self.machining_batch = machining_batch
        self.assembly_batch = assembly_batch