from app.models.Models import RelationPartsxComponents

class RelationPartsxComponents_repositorie:
    def __init__(self, session):
        self.session = session
    


    def create_relation(self, part_ID: int, component_ID: int, qnty:int=1):
        new_relation = RelationPartsxComponents(
            part_ID=part_ID,
            components_ID=component_ID,
            qnty=qnty
        )
        self.session.add(new_relation)
        self.session.commit()
        return new_relation
    
    def get_relations_by_part_id(self, part_ID: int):
        relations = self.session.query(RelationPartsxComponents).filter(RelationPartsxComponents.part_ID==part_ID).all()
        return relations
    

    def delete_relation(self, relation: RelationPartsxComponents):
        self.session.delete(relation)
        self.session.commit()
        return True
    

    def get_all_relations(self):
        relations = self.session.query(RelationPartsxComponents).all()
        return relations
    
    def get_relation_by_component_id(self, component_ID: int):
        relation = self.session.query(RelationPartsxComponents).filter(RelationPartsxComponents.component_ID==component_ID).first()
        return relation