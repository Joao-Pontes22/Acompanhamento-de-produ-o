from app.Schemes.RelationMachinedXRaw_Schemes import RelationMachinedXRaw_Scheme
from app.models.Models import RelationMachinedxRaw


class RelationMachinedxRaw_repositorie:
    def __init__(self, session):
        self.session = session


    def create_relation(self, scheme: RelationMachinedXRaw_Scheme):
        new_relation = RelationMachinedxRaw(
            raw_part_number=scheme.raw_component_id,
            machined_part_number=scheme.machined_component_id,
            qnty=scheme.qnty
        )
        self.session.add(new_relation)
        self.session.commit()
        return new_relation
    

    def get_relation_by_machined_id(self, machined_ID: int):
        relation = self.session.query(RelationMachinedxRaw).filter(RelationMachinedxRaw.machined_ID==machined_ID).first()
        return relation
    
    def get_relation_by_raw_ID(self, raw_ID:int):
        relation = self.session.query(RelationMachinedxRaw).filter(RelationMachinedxRaw.raw_ID==raw_ID).first()
        return relation
    
    def delete_relation(self, machined_component: RelationMachinedxRaw):
        self.session.delete(machined_component)
        self.session.commit()
        return True
    
    def get_all_relations(self):
        relations = self.session.query(RelationMachinedxRaw).all()
        return relations