# Entity for creating a new movimentation record
class Movimentation_entity:
    def __init__(self, part_number: str, origin: str,
                 reason: str, movimentation_type: str,
                 employer: str,
                 qnty: int, date,
                 destination: str,
                batch: str = None,
                 machining_batch: str = None,
                 assembly_batch: str = None):
        self.part_number = part_number
        self.origin = origin
        self.reason = reason
        self.movimentation_type = movimentation_type
        self.employer = employer
        self.batch = batch
        self.machining_batch = machining_batch
        self.assembly_batch = assembly_batch
        self.qnty = qnty
        self.date = date
        self.destination = destination

# Entity for filtering movimentation records
class MovimentationEntityFiltered:
    def __init__(self, part_number: str = None, origin: str = None,
                 batch: str = None,
                 start_date = None,
                 end_date = None,
                 emp_id: int = None,
                 movimentation_type: str = None,
                 destination: str = None,
                 machining_batch: str = None,
                 assembly_batch: str = None):
        self.part_number = part_number.upper() if part_number else None
        self.origin = origin if origin else None
        self.batch = batch if batch else None 
        self.start_date = start_date if start_date else None
        self.end_date = end_date if end_date else None
        self.emp_id = emp_id if emp_id else None
        self.movimentation_type = movimentation_type.upper() if movimentation_type else None
        self.destination = destination
        self.machining_batch = machining_batch.upper() if machining_batch else None
        self.assembly_batch = assembly_batch.upper() if assembly_batch else None