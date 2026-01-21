# Entity for creating a new movimentation record
class MovimentationEntity:
    def __init__(self, 
                 part_number: str, 
                 sector_origin: str,
                 reason: str, 
                 movimentation_type: str,
                 emp_id: str,
                 qnty: int, date,
                 sector_destination: str,
                 batch: str,
                 machining_batch: str,
                 assembly_batch: str
                 ):
        
        self.part_number = part_number
        self.sector_origin = sector_origin
        self.reason = reason
        self.movimentation_type = movimentation_type
        self.emp_id = emp_id
        self.batch = batch
        self.machining_batch = machining_batch
        self.assembly_batch = assembly_batch
        self.qnty = qnty
        self.date = date
        self.sector_destination = sector_destination

# Entity for filtering movimentation records
class MovimentationsEntityFiltred:
    def __init__(self, 
                 part_number: str,
                 sector_origin: str,
                 batch: str ,
                 start_date ,
                 end_date,
                 emp_id: str,
                 movimentation_type: str ,
                 sector_destination: str,
                 machining_batch: str,
                 assembly_batch: str
                 ):
        

        if part_number: 
            self.part_number = part_number.upper()

        if sector_origin: 
            self.origin = sector_origin.upper()

        if batch: 
            self.batch = batch.upper()

        if start_date: 
            self.start_date = start_date

        if end_date:
            self.end_date = end_date

        if emp_id: 
            self.emp_id = emp_id.upper()

        if movimentation_type: 
            self.movimentation_type = movimentation_type.upper()

        if sector_destination: 
            self.sector_destination = sector_destination.upper()

        if machining_batch:
            self.machining_batch = machining_batch.upper()

        if assembly_batch:
            self.assembly_batch = assembly_batch.upper()