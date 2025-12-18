from sqlalchemy .orm import Session
from app.models.Models import ComponentsAndParts
from app.domain.Entitys.Parts_entitys import Parts_entity
class Parts_Repositorie:
    def __init__(self, session:Session):
        self.session = session


    def repo_create_Part(self,scheme: Parts_entity):
        part = ComponentsAndParts(part_number=scheme.part_number,
                                          description=scheme.description_parts,
                                          category="PART",
                                          cost=scheme.cost,
                                          client_ID=scheme.clients_ID,
                                          supplier_ID=None)
        self.session.add(part)
        self.session.commit()
        return part
    
    def repo_get_all_Parts(self):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.category == "PART").all()
    
    def repo_get_Parts_by_id(self, id:int):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.id == id ).first()
    
    def repo_get_Parts_by_part_number(self, part_number:str):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.part_number == part_number).first()

    def repo_update_Part_info(self, part:Parts_Repositorie):
        self.session.commit()
        self.session.refresh(part)
        return part
    
    def repo_delete_part(self, part:Parts_Repositorie):
        self.session.delete(part)
        self.session.commit()
        return(part)