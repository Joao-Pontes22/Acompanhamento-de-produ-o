
from app.domain.Exceptions import NotFoundException
from app.repositories.Movimentation_repositorie import MovimentationRepository
from app.repositories.Parts_repositorie import Parts_Repositorie
from app.repositories.Sectors_repositorie import Sectors_repositorie
from app.repositories.Components_repositorie import Components_Repositorie
from app.domain.Entitys.Movimentation_entity import Movimentation_entity, MovimentationEntityFiltered
class MovimentationService:
    def __init__(self, repo: MovimentationRepository):
        self.repo = repo


    def service_get_all_movimentations(self):
        movimentations = self.repo.get_all()
        return movimentations
    
    def service_get_filtered_movimentations(self, movimentation_id: int,
                                            parts_repo: Parts_Repositorie,
                                           components_repo: Components_Repositorie,
                                           sector_repo: Sectors_repositorie, 
                                           part_number: str = None, 
                                           batch: str = None, 
                                           start_date = None, 
                                           end_date = None, 
                                           employer_id: int = None,
                                           movimentation_type: str = None, 
                                           origin: str = None,
                                           destination: str = None,
                                             machining_batch: str = None,
                                            assembly_batch: str = None
                                           ):
        if movimentation_id is not None:
            movimentation = self.repo.get_by_id(movimentation_id=movimentation_id)
            if not movimentation:
             raise NotFoundException("Movimentation")

        if part_number is not None:
            part = parts_repo.repo_get_Parts_by_part_number(part_number=part_number)
            component = components_repo.repo_get_machined_components(part_number=part_number)
            if not part and not component:
                raise NotFoundException("Part_number")

        if origin is not None:
            origin1 = sector_repo.repo_get_sector_by_id(id=origin)
            if not origin1:
                raise NotFoundException("Origin sector")

        if destination is not None:
            destination1 = sector_repo.repo_get_sector_by_id(id=destination)
            if not destination1:
                raise NotFoundException("Destination sector")
        entity = MovimentationEntityFiltered(part_number=part_number,
                                             origin=origin,
                                             batch=batch,
                                             start_date=start_date,
                                             end_date=end_date,
                                             employer_id=employer_id,
                                             movimentation_type=movimentation_type,
                                             destination=destination,
                                             machining_batch=machining_batch,
                                             assembly_batch=assembly_batch)

        movimentations = self.repo.get_movimentation_filtered(movimentation_id=movimentation_id,
                                                              part_number=entity.part_number,
                                                              batch=entity.batch,
                                                                start_date=entity.start_date,
                                                                end_date=entity.end_date,
                                                                employer_id=entity.employer_id,
                                                                movimentation_type=entity.movimentation_type,
                                                                origin=entity.origin,
                                                                destination=entity.destination,
                                                                machining_batch=entity.machining_batch,
                                                                assembly_batch=entity.assembly_batch)
        return movimentations