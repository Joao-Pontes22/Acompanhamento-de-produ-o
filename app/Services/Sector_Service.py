#Entity
from app.domain.Entitys.Sectors_entitys import SectorsEntity
#Schema
from app.Schemas.Sector_Schemas import SectorSchema, UpdateSectorInfoSchema
#Repository
from app.repositories.Sectors_repository import SectorsRepository
#Exceptions
from app.domain.Exceptions import NotFoundException, AlreadyExist
#Value Objects
from app.domain.Value_objects.Sector import valueSector
#---------------------// SECTOR OPERATIONS //---------------------#
class Sectors_Services():
    def __init__(self,repo: SectorsRepository):
        self.repo = repo
        
    
    def post_sector(self,scheme:SectorSchema):

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
    

    def get_sectors(self):

        sectors = self.repo.get_all_sectors()
        if not sectors:
            raise NotFoundException("Sector")
        
        return sectors


    def get_sector_by_name(self, sector: str):
        
        sector = self.repo.get_sector_by_name(name=sector)
        if not sector:
            raise NotFoundException("Sector")
        
        return sector

    
    
    def update_sector_info(self,sector:str, schema:UpdateSectorInfoSchema):
        value_sector = valueSector(sector_name=sector)
        sector = self.repo.get_sector_by_name(name=value_sector.sector_name)
        if not sector:
            raise NotFoundException("Sector")
        validated = SectorsEntity(sector=schema.sector_name,
                                   tag= schema.tag)
        for field, value in schema.model_dump(exclude_unset=True):
            setattr(sector, field, value)


        updated_sector = self.repo.update_sector_info(sector)
        return updated_sector
        
    def delete_sector(self, sector:str):
        value_sector = valueSector(sector_name=sector)
        sector = self.repo.get_sector_by_name(name=value_sector.sector_name)
        if not sector:
            raise NotFoundException("Sector")
        
        delete  = self.repo.delete_sector(sector=sector)

        return delete
