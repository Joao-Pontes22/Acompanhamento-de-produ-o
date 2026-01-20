
from app.domain.Exceptions import NotFoundException
from app.repositories.Movimentation_repository import MovimentationRepository
from app.repositories.Parts_repository import PartsRepository
from app.repositories.Sectors_repository import SectorsRepository
from app.repositories.Components_repository import ComponentsRepository
from app.domain.Entitys.Movimentation_entity import MovimentationEntity, MovimentationsEntityFiltered
from app.repositories.Employers_repository import EmployersRepository
from app.Schemes.Movimentation_Schemes import MovimentationScheme
class MovimentationService:
    def __init__(self, 
                 repo: MovimentationRepository,
                 parts_repo: PartsRepository,
                 components_repo: ComponentsRepository,
                 sector_repo: SectorsRepository,
                 employer_repo: EmployersRepository
                 ):
        
        self.repo = repo
        self.parts_repo = parts_repo
        self.components_repo = components_repo
        self.sector_repo = sector_repo
        self.employer_repo = employer_repo


    def create_movimentation(self, schema: MovimentationScheme,
                             
                             ):
        entity = MovimentationEntity(part_number=schema.part_number,
                                     qnty=schema.qnty,
                                     batch=schema.batch,
                                     date=schema.date,
                                     emp_id=schema.emp_id,
                                     movimentation_type=schema.movimentation_type,
                                     origin=schema.sector_origin,
                                     destination=schema.sector_destination,
                                     machining_batch=schema.machining_batch,
                                     assembly_batch=schema.assembly_batch
                                     )
        
        part = self.parts_repo.get_part_filtered_first(part_number=entity.part_number)
        component = self.components_repo.get_component_by_part_number(part_number=entity.part_number)
        if not part and not component:
            raise NotFoundException("Part_number")
        
        sector_origin = self.sector_repo.get_sector_by_name(name=entity.origin)
        if not sector_origin:
            raise NotFoundException("Origin sector")
        
        sector_destination = self.sector_repo.get_sector_by_name(name=entity.destination)
        if not sector_destination:
            raise NotFoundException("Destination sector")
        
        employer = self.employer_repo.get_by_emp_id(emp_id=entity.emp_id)
        if not employer:
            raise NotFoundException("Employer")
        
        new_movimentation = self.repo.create_movimentation(part_number=entity.part_number,
                                                           sector_origin=entity.origin,
                                                           reason=entity.reason,
                                                           movimentation_type=entity.movimentation_type,
                                                           emp_id=entity.emp_id,
                                                           batch=entity.batch,
                                                           qnty=entity.qnty,
                                                           date=entity.date,
                                                           sector_destination=entity.destination,
                                                           machining_batch=entity.machining_batch,
                                                           assembly_batch=entity.assembly_batch
                                                           )
        return new_movimentation
    

    def get_all_movimentations(self):
        movimentations = self.repo.get_all()
        return movimentations
    
    def get_filtered_movimentations(self, 
                                    movimentation_id: int,      
                                    part_number: str = None, 
                                    batch: str = None, 
                                    start_date = None, 
                                    end_date = None, 
                                    emp_id: int = None,
                                    movimentation_type: str = None, 
                                    sector_origin: str = None,
                                    destination: str = None,
                                    machining_batch: str = None,
                                    assembly_batch: str = None
                                    ):
        if movimentation_id:
            movimentation = self.repo.get_by_id(movimentation_id=movimentation_id)
            if not movimentation:
             raise NotFoundException("Movimentation")

        if part_number:
            part = self.parts_repo.get_part_filtered_first(part_number=part_number)
            component = self.components_repo.get_component_by_part_number(part_number=part_number)
            if not part and not component:
                raise NotFoundException("Part_number")

        if sector_origin:
            sector_origin_ORM = self.sector_repo.get_sector_by_name(name=sector_origin)
            if not sector_origin_ORM:
                raise NotFoundException("Origin sector")

        if destination:
            destination_ORM = self.sector_repo.get_sector_by_name(name=destination)
            if not destination_ORM:
                raise NotFoundException("Destination sector")
            
        entity = MovimentationsEntityFiltered(part_number=part_number,
                                             origin=sector_origin,
                                             batch=batch,
                                             start_date=start_date,
                                             end_date=end_date,
                                             emp_id=emp_id,
                                             movimentation_type=movimentation_type,
                                             destination=destination,
                                             machining_batch=machining_batch,
                                             assembly_batch=assembly_batch
                                             )

        movimentations = self.repo.get_movimentation_filtered(movimentation_id=movimentation_id,
                                                              part_number=entity.part_number,
                                                              batch=entity.batch,
                                                              start_date=entity.start_date,
                                                              end_date=entity.end_date,
                                                              emp_id=entity.emp_id,
                                                              movimentation_type=entity.movimentation_type,
                                                              origin=entity.origin,
                                                              destination=entity.destination,
                                                              machining_batch=entity.machining_batch,
                                                              assembly_batch=entity.assembly_batch)
        return movimentations
    

    def delete_movimentation(self, movimentation_id: int):
        movimentation = self.repo.get_by_id(movimentation_id=movimentation_id)
        if not movimentation:
            raise NotFoundException("Movimentation")
        deleted_movi = self.repo.delete(movimentation_id=movimentation_id)
        return deleted_movi