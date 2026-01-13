from app.Schemes.Machining_Production_Schemes import Machining_Production_Scheme


class MachiningProductionEntity:
    def __init__(self, scheme: Machining_Production_Scheme):
        self.serial_ID = scheme.serial_ID
        self.sector_ID = scheme.sector_ID
        self.machine_ID = scheme.machine_ID
        self.Date = scheme.Date
        self.duration_process = scheme.duration_process
        self.input_part_number = scheme.input_part_number.upper()
        self.output_part_number = scheme.output_part_number.upper()
        if scheme.machining_batch is not None:
            self.machining_batch = scheme.machining_batch.upper()
        if scheme.assembly_batch is not None:
            self.assembly_batch = scheme.assembly_batch.upper()
        if scheme.warehouse_batch is not None:
            self.warehouse_batch = scheme.warehouse_batch.upper()
        self.emp_id_employer = scheme.emp_id_employer
        self.status = scheme.status.upper()
        
        pass