# Entity for creating or updating a sector
class SectorsEntity:
    def __init__(self, 
                 sector:str, 
                 tag:str):
            
        self.sector = sector
        self.tag = tag

class UpdateSectorsInfoEntity:
    def __init__(self, 
                 sector:str, 
                 tag:str):
        if sector:
            self.sector = sector
        if tag:
            self.tag = tag