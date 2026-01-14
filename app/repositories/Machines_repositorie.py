from typing import List
from app.models.Machines import Machines
from app.domain.Entitys.Machines_entitys import Machine_Entity
from sqlalchemy.orm import Session
class Machine_Repositorie:
    def __init__(self, session:Session):
        self.session = session

    def repo_create_machine(self, scheme:Machine_Entity):
        new_machine = Machines(machine=scheme.Machine,
                               sector_name=scheme.Sector,
                               description_machine=scheme.Description_Machine)

        self.session.add(new_machine)
        self.session.commit()
        return new_machine
    
    def repo_get_all_machine(self):
        machines = self.session.query(Machines).all()
        return machines
    
    
    def get_machine_filtred(self, id: int = None, machine: str = None) -> List[Machines]:
        query = self.session.query(Machines)
        if id:
            query = query.filter(Machines.ID ==id)
        if machine:
            query = query.filter(Machines.machine.like(f"%{machine}%"))
        return query.all()
    
    def get_machine_filtred_first(self, id: int = None, machine: str = None) -> List[Machines]:
        query = self.session.query(Machines)
        if id:
            query = query.filter(Machines.ID ==id)
        if machine:
            query = query.filter(Machines.machine.like(f"%{machine}%"))
        return query.first()
    
    def repo_update_machine_info(self, machine):
        self.session.commit()
        self.session.refresh(machine)
        return machine
    
    def repo_delete_machine(self, machine):
        self.session.delete(machine)
        self.session.commit()
        return machine