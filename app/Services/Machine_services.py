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
        
        validated = Machine_Entity(machine=scheme.machine,
                                   sector=scheme.sector,
                                   description_Machine=scheme.description_machine)
        sector = sectors_repo.repo_get_sector_by_name(name=validated.Sector)
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
    
    def service_get_machine_filtred(self, id:int = None, machine:str = None):
        machine_value = value_Name(name=machine) if machine else None
        machine = self.machine_repo.get_machine_filtred(id=id, machine=machine_value.name if machine_value else None)
        if not machine:
            raise NotFoundException(entity="Machine")
        return machine
    

    def service_delete_machine(self, machine:str):
        machine_value = value_Name(name=machine)
        machine = self.machine_repo.get_machine_filtred_first(machine=machine_value.name)
        if not machine:
            raise NotFoundException(entity="Machine")
        delete = self.machine_repo.repo_delete_machine(machine=machine)
        return delete
    
    def service_update_machine_info(self,machine:str, scheme:Update_Machine_Scheme, sectors_repo:Sectors_repositorie):
        machine_entity = Machine_Entity(
            machine=scheme.machine,
            sector=scheme.sector,
            description_Machine=scheme.description_machine
        )
        if scheme.sector is not None:
            sector = sectors_repo.repo_get_sector_by_name(name=machine_entity.Sector)
            if not sector:
                raise NotFoundException(entity="Sector")
        machine = self.machine_repo.get_machine_filtred_first(machine=machine)
        if not machine:
            raise NotFoundException(entity="Machine")
        if scheme.machine is not None:
            machine.machine = machine_entity.Machine
        
        if scheme.description_machine is not None:
            machine.description_machine = machine_entity.Description_Machine

        if scheme.sector is not None:
            machine.sector_name = machine_entity.Sector
        
        updated = self.machine_repo.repo_update_machine_info(machine=machine)
        return updated