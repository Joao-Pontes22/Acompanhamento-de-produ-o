from typing import List, Optional
from app.models.Relation import Relation


class RelationRepository:
    def __init__(self, session):
        self.session = session
    


    def create_relation(self, 
                        create_item_part_number:str,
                        consume_item_part_number: str,
                        qnty: int
                        ):
        new_relation = Relation(
                                create_item_Part_number=create_item_part_number,
                                consume_item_Part_number=consume_item_part_number,
                                qnty=qnty
                                )
        self.session.add(new_relation)
        self.session.commit()
        return new_relation
    
    def get_relations_filtred(self, 
                              id: int = None, 
                              create_item_part_number: str = None, 
                              consume_item_part_number: str = None
                              ) -> List[Relation]:
        
        query = self.session.query(Relation)
        if id:
            query = query.filter(Relation.ID ==id)
        if create_item_part_number:
            query = query.filter(Relation.create_item_Part_number.like(f"%{create_item_part_number}%"))
        if consume_item_part_number:
            query = query.filter(Relation.consume_item_Part_number.like(f"%{consume_item_part_number}%"))
        return query.all()
    
    def get_relations_filtred_first(self, 
                                    id: Optional[int] = None, 
                                    create_item_part_number: Optional[str] = None, 
                                    consume_item_part_number: Optional[str] = None
                                    ) -> Relation:
        
        query = self.session.query(Relation)
        if id:
            query = query.filter(Relation.ID ==id)
        if create_item_part_number:
            query = query.filter(Relation.create_item_Part_number.like(f"%{create_item_part_number}%"))
        if consume_item_part_number:
            query = query.filter(Relation.consume_item_Part_number.like(f"%{consume_item_part_number}%"))
        return query.first()
    

    def delete_relation(self, relation: Relation):
        self.session.delete(relation)
        self.session.commit()
        return True
    

    def get_all_relations(self):
        relations = self.session.query(Relation).all()
        return relations
    