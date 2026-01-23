#Schema
from app.Schemas.Movimentation_Schemas import MovimentationSchema
from app.Schemas.Queries.movimentation_query_params import MovimentationParameters
#Repository
from app.repositories.Employers_repository import EmployersRepository
from app.repositories.Movimentation_repository import MovimentationRepository
from app.repositories.PartAndComp_repository import PartsAndCompRepository
from app.repositories.Sectors_repository import SectorsRepository

#Exception
from app.domain.Exceptions import NotFoundException
#Entity
from app.domain.Entitys.Movimentation_entity import MovimentationEntity, MovimentationsEntityFiltred


class MovimentationService:
    def __init__(self, 
                 repo: MovimentationRepository,
                 PartOrComp_Repo: PartsAndCompRepository,
                 sector_repo: SectorsRepository,
                 employer_repo: EmployersRepository
                 ):
        
        self.repo = repo
        self.PartOrComp_Repo = PartOrComp_Repo
        self.sector_repo = sector_repo
        self.employer_repo = employer_repo


    def create_movimentation(self, schema: MovimentationSchema,
                             
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
        
        part_or_comp = self.PartOrComp_Repo.get_Parts_and_Components_by_part_number(entity.part_number)
        if not part_or_comp:
            raise NotFoundException("Part_number")
        
        sector_origin = self.sector_repo.get_sector_by_name(name=entity.sector_origin)
        if not sector_origin:
            raise NotFoundException("Origin sector")
        
        sector_destination = self.sector_repo.get_sector_by_name(name=entity.sector_destination)
        if not sector_destination:
            raise NotFoundException("Destination sector")
        
        employer = self.employer_repo.get_by_emp_id(emp_id=entity.emp_id)
        if not employer:
            raise NotFoundException("Employer")
        
        new_movimentation = self.repo.create_movimentation(part_number=entity.part_number,
                                                           sector_origin=entity.sector_origin,
                                                           reason=entity.reason,
                                                           movimentation_type=entity.movimentation_type,
                                                           emp_id=entity.emp_id,
                                                           batch=entity.batch,
                                                           qnty=entity.qnty,
                                                           date=entity.date,
                                                           sector_destination=entity.sector_destination,
                                                           machining_batch=entity.machining_batch,
                                                           assembly_batch=entity.assembly_batch
                                                           )
        return new_movimentation
    

    def get_all_movimentations(self):
        movimentations = self.repo.get_all()
        return movimentations
    
    def get_filtred_movimentations(self, 
                                    query_params: MovimentationParameters
                                    ):
        
        
        if query_params.movimentation_id:
            movimentation = self.repo.get_by_id(movimentation_id=query_params.movimentation_id)
            if not movimentation:
             raise NotFoundException("Movimentation")
            return movimentation

        if query_params.part_number:
            part_or_comp = self.PartOrComp_Repo.get_Parts_and_Components_by_part_number(query_params.part_number)
            if not part_or_comp:
                raise NotFoundException("Part_number")

        if query_params.sector_origin:
            sector_origin_ORM = self.sector_repo.get_sector_by_name(name=query_params.sector_origin)
            if not sector_origin_ORM:
                raise NotFoundException("Origin sector")

        if query_params.sector_destination:
            destination_ORM = self.sector_repo.get_sector_by_name(name=query_params.sector_destination)
            if not destination_ORM:
                raise NotFoundException("Destination sector")
            
        

        movimentations = self.repo.get_movimentation_filtred(
                                                              part_number=query_params.part_number,
                                                              batch=query_params.batch,
                                                              start_date=query_params.start_date,
                                                              end_date=query_params.end_date,
                                                              emp_id=query_params.emp_id,
                                                              movimentation_type=query_params.movimentation_type,
                                                              origin=query_params.sector_origin,
                                                              destination=query_params.sector_destination,
                                                              machining_batch=query_params.machining_batch,
                                                              assembly_batch=query_params.assembly_batch)
        return movimentations
    

    def delete_movimentation(self, movimentation_id: int):
        movimentation = self.repo.get_by_id(movimentation_id=movimentation_id)
        if not movimentation:
            raise NotFoundException("Movimentation")
        deleted_movi = self.repo.delete(movimentation_id=movimentation_id)
        return deleted_movi