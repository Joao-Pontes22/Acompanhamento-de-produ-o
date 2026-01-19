# Entity for creating or updating a sector
class Sector_entitys:
    def __init__(self, sector:str, tag:str):
        if sector is not None:
            self.sector = sector.upper()
        if tag is not None:
            self.tag = tag.upper()