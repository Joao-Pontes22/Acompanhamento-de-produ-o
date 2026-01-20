from app.Schemes.Machining_Production_Schemes import MachiningProductionScheme, MachiningProductionfilteredScheme

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
            self.sector_name = sector_name

        if machine_name: 
            self.machine_name = machine_name

        if date:     
            self.date = date

        if input_part_number:     
            self.input_part_number = input_part_number

        if output_part_number:     
            self.output_part_number = output_part_number

        if  machining_batch: 
            self.machining_batch = machining_batch 

        if batch: 
            self.batch = batch 

        if emp_id: 
            self.emp_id_employer = emp_id 

        if status:
            self.status = status 
