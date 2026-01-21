
# Entity for creating a new machining production record
class MachiningProductionsEntity:
    def __init__(self,
                 sector_name: str,
                 machine_name: str,
                 date,
                 duration_process: int,
                 input_part_number: str,
                 output_part_number: str,
                 batch: str,
                 emp_id: str,
                 status: str
                 ):
        self.sector_name = sector_name
        self.machine_name = machine_name
        self.date = date
        self.duration_process = duration_process
        self.input_part_number = input_part_number
        self.output_part_number = output_part_number
        self.batch = batch
        self.emp_id = emp_id
        self.status = status
    

class MachiningProductionsEntityFiltred:
    def __init__(self,
                 sector_name: str,
                 machine_name: str,
                 date,
                 machining_batch: str,
                 input_part_number: str,
                 output_part_number: str,
                 batch: str,
                 emp_id: str,
                 status: str
                 ):

        if sector_name:
            self.sector_name = sector_name.upper()

        if machine_name: 
            self.machine_name = machine_name.upper()


        if date:     
            self.date = date

        if input_part_number:     
            self.input_part_number = input_part_number.upper()


        if output_part_number:     
            self.output_part_number = output_part_number.upper()


        if  machining_batch: 
            self.machining_batch = machining_batch.upper()


        if batch: 
            self.batch = batch.upper()


        if emp_id: 
            self.emp_id_employer = emp_id.upper()
 

        if status:
            self.status = status.upper()

