from fastapi import  HTTPException
from app.domain.Entitys.Sectors_entitys import Sector_entitys
from app.Schemes.Sector_Schemes import Sector_Scheme, Sector_Scheme_Update
from app.repositories.Sectors_repositorie import Sectors_repositorie
#---------------------// SECTOR OPERATIONS //---------------------#
class Sectors_Services():
    def __init__(self,repo: Sectors_repositorie):
        self.repo = repo
        
    
    def service_get_sectors(self):
        sectors = self.repo.repo_get_all_sectors()
        return sectors


    def service_get_sector_by_id(self, sector_id: int):
        sector = self.repo.repo_get_sector_by_id(id=sector_id)
        return sector

    def service_post_sector(self,scheme:Sector_Scheme):
        new_sector = self.repo.repo_create_sector(Scheme=scheme)
        return new_sector
    
    def service_update_sector_info(self,id:int, scheme:Sector_Scheme_Update):
        sector = self.repo.repo_get_sector_by_id(id=id)
        if not sector:
            raise HTTPException(status_code=401, detail="Sector not found")
        validated = Sector_entitys(sector=scheme.sector,
                                   tag= scheme.tag)
        if scheme.sector is not None:
            sector.sector = validated.sector
        if scheme.tag is not None:
            sector.tag = validated.tag

        updated_sector = self.repo.repo_update_sector_info(sector)
        return updated_sector
        
    def service_delete_sector(self, id:int):
        sector = self.repo.repo_get_sector_by_id(id=id)
        delete  = self.repo.repo_delete_sector(sector=sector)
        return delete
