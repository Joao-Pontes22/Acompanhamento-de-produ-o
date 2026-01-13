from app.repositories.Machining_Production_repositorie import Machining_ProductionRepositorie
from app.domain.Entitys.Machining_Production_entitys import MachiningProductionEntity
from app.repositories.RelationMachinedxRaw_repositorie import RelationMachinedxRaw_repositorie
from app.repositories.Employers_repositories import employersRepo
from app.repositories.Machines_repositorie import Machine_Repositorie
from app.repositories.Sectors_repositorie import Sectors_repositorie
from app.domain.Exceptions import NotFoundException, AlreadyExist

class MachiningProductionServices:
    def __init__(self, Machining_Production_repo: Machining_ProductionRepositorie):
        self.Machining_Production_repo = Machining_Production_repo


    def service_create_machining_production(self, Scheme, 
                                            relation_repo: RelationMachinedxRaw_repositorie,
                                             sector_repo: Sectors_repositorie, 
                                             machine_repo: Machine_Repositorie, employer_repo: employersRepo):
        entity = MachiningProductionEntity(Scheme)
        input_component = relation_repo.get_relation_by_raw_ID(entity.input_part_number)
        if not input_component:
            raise NotFoundException("Raw Component")
        if input_component.