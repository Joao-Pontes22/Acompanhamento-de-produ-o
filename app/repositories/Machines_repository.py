from typing import List
from app.models.Machines import Machines
from sqlalchemy.orm import Session


class MachineRepository:
    def __init__(self, session:Session):
        self.session = session

    def create_machine(self,
                            machine:str,
                            sector_name: str,
                            description_machine: str):
        
        new_machine = Machines(machine=machine,
                               sector_name=sector_name,
                               description_machine=description_machine)

        self.session.add(new_machine)
        self.session.commit()
        return new_machine
    
    def get_all_machine(self):
        machines = self.session.query(Machines).all()
        return machines
    
    
    def get_machine_filtred(self, 
                            id: int = None, 
                            machine: str = None) -> List[Machines]:
        
        query = self.session.query(Machines)
        if id:
            query = query.filter(Machines.ID ==id)
        if machine:
            query = query.filter(Machines.machine.like(f"%{machine}%"))
        return query.all()
    
    def get_machine_filtred_first(self, 
                                  id: int = None, 
                                  machine: str = None) -> Machines:
        
        query = self.session.query(Machines)
        if id:
            query = query.filter(Machines.ID ==id)
        if machine:
            query = query.filter(Machines.machine.like(f"%{machine}%"))
        return query.first()
    
    def update_machine_info(self, machine):

        self.session.commit()
        self.session.refresh(machine)
        return machine
    
    def delete_machine(self, machine):

        self.session.delete(machine)
        self.session.commit()
        return machine