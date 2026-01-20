from app.domain.Entitys.Sectors_entitys import SectorsEntity
from app.Schemes.Sector_Schemes import SectorScheme, UpdateSectorInfoScheme
from app.repositories.Sectors_repository import SectorsRepository
from app.domain.Exceptions import NotFoundException, AlreadyExist
#---------------------// SECTOR OPERATIONS //---------------------#
class Sectors_Services():
    def __init__(self,repo: SectorsRepository):
        self.repo = repo
        
    
    def service_get_sectors(self):

        sectors = self.repo.get_all_sectors()
        if not sectors:
            raise NotFoundException("Sector")
        
        return sectors


    def service_get_sector_by_name(self, sector: str):
        
        sector = self.repo.get_sector_by_name(name=sector)
        if not sector:
            raise NotFoundException("Sector")
        
        return sector

    def service_post_sector(self,scheme:SectorScheme):

        entity = SectorsEntity(sector=scheme.sector_name,
                                tag= scheme.tag)
        sector = self.repo.get_sector_by_name(name=entity.sector)
        if sector:
            raise AlreadyExist("Sector")
        tag = self.repo.get_sector_by_tag(tag=entity.tag)
        if tag:
            raise AlreadyExist("Tag")
        new_sector = self.repo.create_sector(Scheme=entity)
        return new_sector
    
    def service_update_sector_info(self,sector:str, schema:UpdateSectorInfoScheme):
        sector = self.repo.get_sector_by_name(name=schema.sector_name)
        if not sector:
            raise NotFoundException("Sector")
        validated = SectorsEntity(sector=schema.sector_name,
                                   tag= schema.tag)
        if schema.sector_name:
            sector.sector = validated.sector
        if schema.tag:
            sector.tag = validated.tag

        updated_sector = self.repo.update_sector_info(sector)
        return updated_sector
        
    def service_delete_sector(self, sector:str):
        sector = self.repo.get_sector_by_name(name=sector)
        if not sector:
            raise NotFoundException("Sector")
        delete  = self.repo.delete_sector(sector=sector)
        return delete
