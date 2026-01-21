# Entity for transferring items between sectors
class TransferEntity:
    def __init__(self, 
                 part_number: str,
                 origin_sector: str,
                 destination_sector: str,
                 qnty: int,
                 reason: str,
                 batch: str = None,
                 machining_batch: str = None,
                 assembly_batch: str = None
                 ):
        
        self.part_number = part_number
        self.origin_sector = origin_sector
        self.destination_sector = destination_sector
        self.qnty = qnty
        self.reason = reason

        if batch:
            self.batch = batch

        if machining_batch:
            self.machining_batch = machining_batch 

        if assembly_batch:
            self.assembly_batch = assembly_batch