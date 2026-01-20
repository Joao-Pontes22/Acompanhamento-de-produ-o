from app.Schemes.Machine_Schemes import MachineScheme, UpdateMachineInfoScheme
from app.domain.Entitys.Machines_entitys import MachineEntity
from app.repositories.Machines_repository import MachineRepository
from app.repositories.Sectors_repository import SectorsRepository
from app.domain.Exceptions import NotFoundException
from app.domain.Exceptions import AlreadyExist

class ServiceMachines:
    def __init__(self,machine_repo:MachineRepository):
        self.machine_repo = machine_repo
    

    def create_machine(self, 
                       scheme:MachineScheme, 
                       sectors_repo: SectorsRepository
                       ):
        
        entity = MachineEntity(machine_name=scheme.machine,
                                   sector_name=scheme.sector_name,
                                   description_machine=scheme.description_machine
                                )
        
        sector = sectors_repo.get_sector_by_name(name=entity.sector_name)
        if not sector:
            raise NotFoundException(entity="Sector")
        
        existing_machine = self.machine_repo.get_machine_filtred_first(entity.machine_name)
        if existing_machine:
            raise AlreadyExist(entity="Machine")
        
        new_machine = self.machine_repo.create_machine(machine=entity.machine_name,
                                                            sector_name=entity.sector_name,
                                                            description_machine=entity.description_machine
                                                            )
        return new_machine
    
    def get_all_machines(self):

        machines = self.machine_repo.get_all_machine()
        if not machines:
            raise NotFoundException(entity="Machines")
        
        return machines
    
    def get_machine_filtered(self, id:int, machine:str):

        machine = self.machine_repo.get_machine_filtred(id=id, machine=machine)

        if not machine:
            raise NotFoundException(entity="Machine")
        
        return machine
    

    def delete_machine(self, machine:str):

        machine = self.machine_repo.get_machine_filtred_first(machine=machine)
        if not machine:
            raise NotFoundException(entity="Machine")
        
        delete = self.machine_repo.delete_machine(machine=machine)

        return delete
    

    def update_machine_info(self,machine:str, schema:UpdateMachineInfoScheme, sectors_repo:SectorsRepository):
        

        if schema.sector_name:
            sector = sectors_repo.get_sector_by_name(name=schema.sector_name)
            if not sector:
                raise NotFoundException(entity="Sector")
            
        machine = self.machine_repo.get_machine_filtred_first(machine=machine)
        if not machine:
            raise NotFoundException(entity="Machine")
        
        for field, value, in schema.model_dump(exclude_unset=True).items():
            setattr(machine, field, value )
        
        updated = self.machine_repo.update_machine_info(machine=machine)
        return updated