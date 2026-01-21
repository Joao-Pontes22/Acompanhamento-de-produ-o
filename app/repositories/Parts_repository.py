from sqlalchemy .orm import Session
from app.models.ComponentsAndParts import ComponentsAndParts


class PartsRepository:
    def __init__(self, session:Session):
        self.session = session


    def create_part(self,
                         part_number: str,
                         description_parts: str,
                         cost: float,
                         client_name: str
                         )-> ComponentsAndParts :
        
        part = ComponentsAndParts(part_number=part_number,
                                          description=description_parts,
                                          category="PART",
                                          cost=cost,
                                          client_name=client_name,
                                          supplier_name=None
                                          )
        self.session.add(part)
        self.session.commit()
        return part
    
    def get_all_parts(self)-> list[ComponentsAndParts]:
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.category == "PART").all()
    
    def update_part_info(self, part) -> ComponentsAndParts:
        self.session.commit()
        self.session.refresh(part)
        return part
    
    def delete_part(self, part)-> ComponentsAndParts:
        self.session.delete(part)
        self.session.commit()
        return(part)
    
    def get_parts_filtred(self, 
                              id:int = None, 
                              part_number:str = None, 
                              description:str = None, 
                              client:str = None
                              )-> list[ComponentsAndParts]:
        
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
    
    def get_part_filtred_first(self, 
                                id:int = None, 
                                part_number:str = None, 
                                description:str = None, 
                                client:str = None
                                ) -> ComponentsAndParts:
        
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