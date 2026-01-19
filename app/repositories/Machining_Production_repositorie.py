from app.models.Machining_production import Machining_Production
from app.Schemes.Machining_Production_Schemes import Machining_Production_Scheme


class Machining_ProductionRepositorie:
    def __init__(self, session):
        self.session = session
    
    def repo_create_machining_production(self, Scheme: Machining_Production_Scheme, serial_id: int):
        new_machining_production = Machining_Production(
            serial_ID=serial_id,
            sector_ID=Scheme.sector_name,
            machine_ID=Scheme.machine_name,
            Date=Scheme.Date,
            duration_process=Scheme.duration_process,
            input_part_number=Scheme.input_part_number,
            output_part_number=Scheme.output_part_number,
            warehouse_batch=Scheme.batch,
            emp_id_employer=Scheme.emp_id_employer,
            status=Scheme.status,
            )
        self.session.add(new_machining_production)
        self.session.commit()
        self.session.refresh(new_machining_production)
        return new_machining_production
    
    def repo_get_all_machining_production(self):
        machining_production = self.session.query(Machining_Production).all()
        return machining_production
    
    def repo_get_machining_procutions_filtred(self, sector_name: str = None, 
                                              machine_name: str = None,
                                              batch: str = None,
                                              input_part_number: str = None,
                                              output_part_number: str = None,
                                              machining_batch: str = None,
                                              emp_id_employer: str = None,
                                              status: str = None):
        query = self.session.query(Machining_Production)
        
        if sector_name is not None:
            query = query.filter(Machining_Production.sector_name == sector_name)
        
        if machine_name is not None:
            query = query.filter(Machining_Production.machine_name == machine_name)
        if batch is not None:
            query = query.filter(Machining_Production.batch == batch)
        if input_part_number is not None:
            query = query.filter(Machining_Production.input_part_number == input_part_number)
        if output_part_number is not None:
            query = query.filter(Machining_Production.output_part_number == output_part_number)
        if machining_batch is not None:
            query = query.filter(Machining_Production.machining_batch == machining_batch)
        if emp_id_employer is not None:
            query = query.filter(Machining_Production.emp_id_employer == emp_id_employer)
        if status is not None:
            query = query.filter(Machining_Production.status == status)
        
        results = query.all()
        return results