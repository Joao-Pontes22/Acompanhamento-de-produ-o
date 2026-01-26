#Repositories
from app.repositories.Setup_repository import SetupRepository
from app.repositories.Employers_repository import EmployersRepository
from app.repositories.PartAndComp_repository import PartsAndCompRepository
from app.repositories.Machines_repository import MachineRepository
#Schema
from app.Schemas.Setup_Schema import SetupSchema
from app.Schemas.Queries.setup_query_params import SetupQueryParams
#Entity
from app.domain.Entitys.Setup_entitys import SetupEntity
#Exceptions
from app.domain.Exceptions import NotFoundException


class SetupService:
    def __init__(self, Setup_repo: SetupRepository):
        self.setup_repo = Setup_repo




    def create_setup(self,
                    schema:SetupSchema,
                    machine_repo: MachineRepository,
                    partsorcomp_repo: PartsAndCompRepository,
                    employers_repo: EmployersRepository ):
        entity = SetupEntity(machine=schema.machine,
                             part_number=schema.part_number,
                             date=schema.Date,
                             Emp_id=schema.Emp_id,
                             Notes=schema.Notes)
        
        machine = machine_repo.get_machine_filtred_first(machine=entity.machine)
        if not machine:
            raise NotFoundException(entity="Machine")
        
        partorcomp = partsorcomp_repo.get_Parts_and_Components_by_part_number(part_number=entity.part_number)
        if not partorcomp:
            raise NotFoundException(entity="Part Number")
        
        employer = employers_repo.get_employer_filtred(emp_id=entity.Emp_id)
        if not employer:
            raise NotFoundException
        
        new_setup = self.setup_repo.create_setup(entity=entity)
        return new_setup

    def get_all_setups(self):
        setups = self.setup_repo.get_all_setups()
        if not setups:
            raise NotFoundException(entity="Setups")
        return setups
    

    def get_setup_filtered(self, 
                           query_params: SetupQueryParams):
        setups = self.setup_repo.get_setup_filtered(machine=query_params.machine,
                                                    part_number=query_params.part_number,
                                                    date=query_params.date,
                                                    emp_id=query_params.Emp_id)
        if not setups:
            raise NotFoundException(entity="Setups")
        return setups
        

        