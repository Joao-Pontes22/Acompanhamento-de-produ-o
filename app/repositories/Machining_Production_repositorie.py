from app.models.Models import Machining_Production
from app.Schemes.Machining_Production_Schemes import Machining_Production_Scheme


class Machining_ProductionRepositorie:
    def __init__(self, session):
        self.session = session
    
    def repo_create_machining_production(self, Scheme: Machining_Production_Scheme):
        new_machining_production = Machining_Production(
            serial_ID=Scheme.serial_ID,
            sector_ID=Scheme.sector_ID,
            machine_ID=Scheme.machine_ID,
            Date=Scheme.Date,
            duration_process=Scheme.duration_process,
            input_part_number=Scheme.input_part_number,
            output_part_number=Scheme.output_part_number,
            machining_batch=Scheme.machining_batch,
            assembly_batch=Scheme.assembly_batch,
            warehouse_batch=Scheme.warehouse_batch,
            emp_id_employer=Scheme.emp_id_employer,
            status=Scheme.status,
            )
        self.session.add(new_machining_production)
        self.session.commit()
        self.session.refresh(new_machining_production)
        return new_machining_production