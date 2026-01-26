
# Entity for creating a new machining production record
class MachiningProductionsEntity:
    def __init__(self,
                 sector_name: str,
                 machine_name: str,
                 date,
                 duration_process: int,
                 input_part_number: str,
                 output_part_number: str,
                 setup: str,
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
        self.setup = setup
        self.emp_id = emp_id
        self.status = status
        self.batch = batch
    



