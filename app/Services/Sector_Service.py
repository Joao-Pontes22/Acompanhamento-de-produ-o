from fastapi import  HTTPException
from app.domain.Entitys.Sectors_entitys import Sector_entitys
from app.Schemes.Sector_Schemes import Sector_Scheme, Sector_Scheme_Update
from app.repositories.Sectors_repositorie import Sectors_repositorie
from app.domain.Exceptions import NotFoundException, AlreadyExist
from app.domain.Value_objects import Sector
#---------------------// SECTOR OPERATIONS //---------------------#
class Sectors_Services():
    def __init__(self,repo: Sectors_repositorie):
        self.repo = repo
        
    
    def service_get_sectors(self):
        sectors = self.repo.repo_get_all_sectors()
        if not sectors:
            raise NotFoundException("Sector")
        return sectors


    def service_get_sector_by_name(self, sector: str):
        validated_sector = Sector.value_Sector(sector)
        sector = self.repo.repo_get_sector_by_name(name=validated_sector.sector)
        if not sector:
            raise NotFoundException("Sector")
        return sector

    def service_post_sector(self,scheme:Sector_Scheme):
        entity = Sector_entitys(sector=scheme.sector,
                                    tag= scheme.tag)
        sector = self.repo.repo_get_sector_by_name(name=entity.sector)
        if sector:
            raise AlreadyExist("Sector")
        tag = self.repo.repo_get_sector_by_tag(tag=entity.tag)
        if tag:
            raise AlreadyExist("Tag")
        new_sector = self.repo.repo_create_sector(Scheme=entity)
        return new_sector
    
    def service_update_sector_info(self,sector:str, scheme:Sector_Scheme_Update):
        validated_sector = Sector.value_Sector(sector)
        sector = self.repo.repo_get_sector_by_name(name=validated_sector.sector)
        if not sector:
            raise NotFoundException("Sector")
        validated = Sector_entitys(sector=scheme.sector,
                                   tag= scheme.tag)
        if scheme.sector is not None:
            sector.sector = validated.sector
        if scheme.tag is not None:
            sector.tag = validated.tag

        updated_sector = self.repo.repo_update_sector_info(sector)
        return updated_sector
        
    def service_delete_sector(self, sector:str):
        validated_sector = Sector.value_Sector(sector)
        sector = self.repo.repo_get_sector_by_name(name=validated_sector.sector)
        if not sector:
            raise NotFoundException("Sector")
        delete  = self.repo.repo_delete_sector(sector=sector)
        return delete
