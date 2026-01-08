from fastapi import HTTPException
from app.Schemes.Machine_Schemes import Machine_Scheme, Update_Machine_Scheme
from app.domain.Entitys.Machines_entitys import Machine_Entity
from app.repositories.Machines_repositorie import Machine_Repositorie
from app.repositories.Sectors_repositorie import Sectors_repositorie
from app.domain.Value_objects.Machine import value_Name
from app.domain.Exceptions import NotFoundException
class Service_Machines:
    def __init__(self,machine_repo:Machine_Repositorie):
        self.machine_repo = machine_repo
    

    def service_create_machine(self, scheme:Machine_Scheme, sectors_repo: Sectors_repositorie):
        sector = sectors_repo.repo_get_sector_by_id(id=scheme.sector_ID)
        validated = Machine_Entity(machine=scheme.machine,
                                   sector_ID=scheme.sector_ID,
                                   description_Machine=scheme.description_machine)
        if not sector:
            raise NotFoundException(entity="Sector")
        # Check if machine already exists
        existing_machine = self.machine_repo.repo_get_machine_by_name(validated.Machine)
        if existing_machine:
            from app.domain.Exceptions import AlreadyExist
            raise AlreadyExist(entity="Machine")
        new_machine = self.machine_repo.repo_create_machine(scheme=validated)
        return new_machine
    
    def service_get_all_machines(self):
        machines = self.machine_repo.repo_get_all_machine()
        if not machines:
            raise NotFoundException(entity="Machines")
        return machines
    
    def service_get_machine_by_id(self, id:int):
        machine = self.machine_repo.repo_get_machine_by_id(id=id)
        if not machine:
            raise NotFoundException(entity="Machine")
        return machine
    
    def service_get_machine_by_name(self, name:str):
        Value_machine = value_Name(name=name)
        machine = self.machine_repo.repo_get_machine_by_name(name=Value_machine.name)
        if not machine:
            raise NotFoundException(entity="Machine")
        return machine

    def service_delete_machine(self, id:int):
        machine = self.machine_repo.repo_get_machine_by_id(id=id)
        if not machine:
            raise NotFoundException(entity="Machine")
        delete = self.machine_repo.repo_delete_machine(machine=machine)
        return delete
    
    def service_update_machine_info(self,id:int, scheme:Update_Machine_Scheme, sectors_repo:Sectors_repositorie):
        sector = sectors_repo.repo_get_sector_by_id(id=scheme.sector_ID)
        machine = self.machine_repo.repo_get_machine_by_id(id=id)
        validated = Machine_Entity(machine=scheme.machine,
                                   sector_ID=scheme.sector_ID,
                                   description_Machine=scheme.description_machine)
        if not machine:
            raise NotFoundException(entity="Machine")
        if not sector:
            raise NotFoundException(entity="Sector")
        
        if scheme.machine is not None:
            machine.machine = validated.Machine
        
        if scheme.description_machine is not None:
            machine.description_machine = validated.Description_Machine
        
        if scheme.sector_ID is not None:
            machine.sector_ID = validated.Sector_ID
        
        updated = self.machine_repo.repo_update_machine_info(machine=machine)
        return updated