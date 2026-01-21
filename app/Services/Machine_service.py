#Schemas
from app.Schemas.Machine_Schemas import MachineSchema, UpdateMachineInfoSchema
#Entity
from app.domain.Entitys.Machines_entitys import MachineEntity
#Repository
from app.repositories.Machines_repository import MachineRepository
from app.repositories.Sectors_repository import SectorsRepository
#Exceptions
from app.domain.Exceptions import NotFoundException, AlreadyExist
#Value Objects
from app.domain.Value_objects.Machine import ValueMachine

class MachineService:
    def __init__(self,machine_repo:MachineRepository):
        self.machine_repo = machine_repo
    

    def create_machine(self, 
                       scheme:MachineSchema, 
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
    
    def get_machine_filtred(self, 
                            id:int = None, 
                            machine:str = None):
        if machine:
            value_machine = ValueMachine(machine=machine)
        machine = self.machine_repo.get_machine_filtred(id=id, machine=value_machine.machine)

        if not machine:
            raise NotFoundException(entity="Machine")
        
        return machine
    

    def delete_machine(self, machine:str):
        value_machine = ValueMachine(machine=machine)
        machine = self.machine_repo.get_machine_filtred_first(machine=value_machine.machine)
        if not machine:
            raise NotFoundException(entity="Machine")
        
        delete = self.machine_repo.delete_machine(machine=machine)

        return delete
    

    def update_machine_info(self,machine:str, schema:UpdateMachineInfoSchema, sectors_repo:SectorsRepository):
        
        value_machine = ValueMachine(machine=machine)
        machine = self.machine_repo.get_machine_filtred_first(machine=value_machine.machine)
        if not machine:
            raise NotFoundException(entity="Machine")
        
        if schema.sector_name:
            sector = sectors_repo.get_sector_by_name(name=schema.sector_name)
            if not sector:
                raise NotFoundException(entity="Sector")
            
        for field, value, in schema.model_dump(exclude_unset=True).items():
            setattr(machine, field, value )
        
        updated = self.machine_repo.update_machine_info(machine=machine)
        return updated