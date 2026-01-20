# Entity for creating a new movimentation record
class MovimentationEntity:
    def __init__(self, 
                 part_number: str, 
                 origin: str,
                 reason: str, 
                 movimentation_type: str,
                 emp_id: str,
                 qnty: int, date,
                 destination: str,
                 batch: str,
                 machining_batch: str,
                 assembly_batch: str
                 ):
        
        self.part_number = part_number
        self.origin = origin
        self.reason = reason
        self.movimentation_type = movimentation_type
        self.emp_id = emp_id
        self.batch = batch
        self.machining_batch = machining_batch
        self.assembly_batch = assembly_batch
        self.qnty = qnty
        self.date = date
        self.destination = destination

# Entity for filtering movimentation records
class MovimentationsEntityFiltered:
    def __init__(self, 
                 part_number: str,
                 origin: str,
                 batch: str ,
                 start_date ,
                 end_date,
                 emp_id: int,
                 movimentation_type: str ,
                 destination: str,
                 machining_batch: str,
                 assembly_batch: str
                 ):
        

        if part_number: 
            self.part_number = part_number

        if origin: 
            self.origin = origin

        if batch: 
            self.batch = batch

        if start_date: 
            self.start_date = start_date 

        if end_date:
            self.end_date = end_date

        if emp_id: 
            self.emp_id = emp_id

        if movimentation_type: 
            self.movimentation_type = movimentation_type

        if destination: 
            self.destination = destination

        if machining_batch:
            self.machining_batch = machining_batch 

        if assembly_batch:
            self.assembly_batch = assembly_batch 