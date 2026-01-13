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
                                          client_name=scheme.client,
                                          supplier_name=None)
        self.session.add(part)
        self.session.commit()
        return part
    
    def repo_get_all_Parts(self):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.category == "PART").all()
    
    def repo_update_Part_info(self, part):
        self.session.commit()
        self.session.refresh(part)
        return part
    
    def repo_delete_part(self, part):
        self.session.delete(part)
        self.session.commit()
        return(part)
    
    def repo_get_part_filteres(self, id:int = None, part_number:str = None, description:str = None, client:str = None):
        query = self.session.query(ComponentsAndParts).filter(ComponentsAndParts.category == "PART")
        if id:
            query = query.filter(ComponentsAndParts.id ==id)
        if part_number:
            query = query.filter(ComponentsAndParts.part_number.like(f"%{part_number}%"))
        if description:
            query = query.filter(ComponentsAndParts.description.like(f"%{description}%"))
        if client:
            query = query.filter(ComponentsAndParts.client_name == client)
        return query.all()
    
    def repo_get_part_filtered_first(self, id:int = None, part_number:str = None, description:str = None, client:str = None):
        query = self.session.query(ComponentsAndParts).filter(ComponentsAndParts.category == "PART")
        if id:
            query = query.filter(ComponentsAndParts.id ==id)
        if part_number:
            query = query.filter(ComponentsAndParts.part_number.like(f"%{part_number}%"))
        if description:
            query = query.filter(ComponentsAndParts.description.like(f"%{description}%"))
        if client:
            query = query.filter(ComponentsAndParts.client_name == client)
        return query.first()