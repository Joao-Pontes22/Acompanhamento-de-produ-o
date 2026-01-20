from app.models.Machining_production import MachiningProduction


class Machining_ProductionRepository:
    def __init__(self, session):
        self.session = session
    
    def create_machining_production(self,
                                        sector_name: str,
                                        machine_name: str,
                                        date,
                                        duration_process: int,
                                        input_part_number: str,
                                        output_part_number: str,
                                        batch: str,
                                        emp_id: str,
                                        status: str,
                                        serial_id: int):
        
        new_machining_production = MachiningProduction( serial_ID=serial_id,
                                                        sector_ID=sector_name,
                                                        machine_ID=machine_name,
                                                        Date=date,
                                                        duration_process=duration_process,
                                                        input_part_number=input_part_number,
                                                        output_part_number=output_part_number,
                                                        warehouse_batch=batch,
                                                        emp_id_employer=emp_id,
                                                        status=status,
                                                        )
        self.session.add(new_machining_production)
        self.session.commit()
        self.session.refresh(new_machining_production)
        return new_machining_production
    
    def get_all_machining_production(self):
        machining_production = self.session.query(MachiningProduction).all()
        return machining_production
    
    def get_machining_productions_filtered(self, sector_name: str, 
                                              machine_name: str,
                                              batch: str,
                                              input_part_number: str,
                                              output_part_number: str,
                                              machining_batch: str,
                                              emp_id_employer: str,
                                              status: str
                                              ):
        query = self.session.query(MachiningProduction)
        
        if sector_name:
            query = query.filter(MachiningProduction.sector_name == sector_name)
        
        if machine_name:
            query = query.filter(MachiningProduction.machine_name == machine_name)
        if batch:
            query = query.filter(MachiningProduction.batch == batch)
        if input_part_number:
            query = query.filter(MachiningProduction.input_part_number == input_part_number)
        if output_part_number:
            query = query.filter(MachiningProduction.output_part_number == output_part_number)
        if machining_batch:
            query = query.filter(MachiningProduction.machining_batch == machining_batch)
        if emp_id_employer:
            query = query.filter(MachiningProduction.emp_id_employer == emp_id_employer)
        if status:
            query = query.filter(MachiningProduction.status == status)
        
        results = query.all()
        return results