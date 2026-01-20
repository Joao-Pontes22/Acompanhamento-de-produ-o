from app.models.Sectors import Sectors


class SectorsRepository:
    def __init__(self, session):
        self.session = session
    

    def create_sector(self, 
                           sector_name: str,
                           tag: str
                           ):
        
        new_sector = Sectors(sector=sector_name,
                             tag=tag
                             )
        
        self.session.add(new_sector)
        self.session.commit()
        self.session.refresh(new_sector)
        return new_sector

    def get_all_sectors(self):
        sector = self.session.query(Sectors).all()
        return sector
    
    def get_sector_by_name(self, name:str):
        sector =  self.session.query(Sectors).filter(Sectors.sector == name).first()
        return sector
    
    def get_sector_by_tag(self, tag:str):
        sector =  self.session.query(Sectors).filter(Sectors.tag == tag).first()
        return sector
    
    def get_sector_by_id(self, id:int):
        sector =  self.session.query(Sectors).filter(Sectors.ID == id).first()
        return sector
    
    def update_sector_info(self, sector):
        self.session.commit()
        self.session.refresh(sector)
        return sector

    def delete_sector(self, sector):
        self.session.delete(sector)
        self.session.commit()
        return sector
