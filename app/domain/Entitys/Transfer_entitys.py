class Transfer_entitys:
    def __init__(self, 
                 part_number: str,
                 origin_sector: str,
                 destination_sector: str,
                 qnty: int,
                 reason: str,
                 batch: str = None,
                 machining_batch: str = None,
                 assembly_batch: str = None):
        self.part_number = part_number.upper()
        self.origin_sector = origin_sector.upper()
        self.destination_sector = destination_sector.upper()
        self.qnty = qnty
        self.reason = reason
        self.batch = batch.upper() if batch else None
        self.machining_batch = machining_batch.upper() if machining_batch else None
        self.assembly_batch = assembly_batch.upper() if assembly_batch else None