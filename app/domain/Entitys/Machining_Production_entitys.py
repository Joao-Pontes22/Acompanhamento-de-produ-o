from app.Schemes.Machining_Production_Schemes import Machining_Production_Scheme, Machining_Production_filtred_Scheme

# Entity for creating a new machining production record
class MachiningProductionEntity:
    def __init__(self, scheme: Machining_Production_Scheme):
        self.sector_name = scheme.sector_name
        self.machine_name = scheme.machine_name
        self.Date = scheme.Date
        self.duration_process = scheme.duration_process
        self.input_part_number = scheme.input_part_number.upper()
        self.output_part_number = scheme.output_part_number.upper()
        self.batch = scheme.batch.upper()
        self.emp_id_employer = scheme.emp_id_employer.upper()
        self.status = scheme.status.upper()
    

class MachiningProductionEntityFiltred:
    def __init__(self, sector_name : str = None,
                 machine_name : str = None,
                 Date : str = None,
                 input_part_number : str = None,
                 output_part_number : str = None,
                 machining_batch : str = None,
                 batch : str = None,
                 emp_id_employer : str = None,
                 status : str = None):
        self.sector_name = sector_name if sector_name else None
        self.machine_name = machine_name if machine_name else None
        self.Date = Date if Date else None
        self.input_part_number = input_part_number.upper() if input_part_number else None
        self.output_part_number = output_part_number.upper() if output_part_number else None
        if machining_batch is not None:
            self.machining_batch = machining_batch.upper()
        if batch is not None:
            self.batch = batch.upper()
        self.emp_id_employer = emp_id_employer.upper() if emp_id_employer else None
        self.status = status.upper() if status else None
