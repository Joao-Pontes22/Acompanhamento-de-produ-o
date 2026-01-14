from app.models.Sectors import Sectors
from app.Schemes.Sector_Schemes import Sector_Scheme, Sector_Scheme_Update
from app.domain.Entitys.Sectors_entitys import Sector_entitys

class Sectors_repositorie:
    def __init__(self, session):
        self.session = session
    

    def repo_create_sector(self, Scheme: Sector_entitys):
        new_sector = Sectors(sector=Scheme.sector,
                             tag=Scheme.tag
                             )
        self.session.add(new_sector)
        self.session.commit()
        self.session.refresh(new_sector)
        return new_sector

    def repo_get_all_sectors(self):
        sector = self.session.query(Sectors).all()
        return sector
    
    def repo_get_sector_by_name(self, name:str):
        sector =  self.session.query(Sectors).filter(Sectors.sector == name).first()
        return sector
    
    def repo_get_sector_by_tag(self, tag:str):
        sector =  self.session.query(Sectors).filter(Sectors.tag == tag).first()
        return sector
    
    def repo_get_sector_by_id(self, id:int):
        sector =  self.session.query(Sectors).filter(Sectors.ID == id).first()
        return sector
    
    def repo_update_sector_info(self, sector):
        self.session.commit()
        self.session.refresh(sector)
        return sector

    def repo_delete_sector(self, sector):
        self.session.delete(sector)
        self.session.commit()
        return sector
