from app.models.Models import Machines
from app.Schemes.Machine_Schemes import Machine_Scheme
from sqlalchemy.orm import Session
class Machine_Repositorie:
    def __init__(self, session:Session):
        self.session = session

    
    def repo_create_machine(self, scheme:Machine_Scheme):
        new_machine = Machines(machine=scheme.Machine,
                               sector_ID=scheme.Sector_ID,
                               description_machine=scheme.Description_Machine)

        self.session.add(new_machine)
        self.session.commit()
        return new_machine
    
    def repo_get_all_machine(self):
        machines = self.session.query(Machines).all()
        return machines
    
    def repo_get_machine_by_name(self, name:str):
        machines = self.session.query(Machines).filter(Machines.machine == name).first()
        return machines
    
    def repo_get_machine_by_id(self, id:int):
        machines = self.session.query(Machines).filter(Machines.ID == id).first()
        return machines
    
    def repo_update_machine_info(self, machine):
        self.session.commit()
        self.session.refresh(machine)
        return machine
    
    def repo_delete_machine(self, machine):
        self.session.delete(machine)
        self.session.commit()
        return machine