
from app.models.Models import RelationPartsxComponents
from app.repositories.RelationPartsxComponents_repositorie import RelationPartsxComponents_repositorie


class RelationPartsxComponents_Services:
    def __init__(self, relation_repo: RelationPartsxComponents_repositorie):
        self.relation_repo = relation_repo



    def service_create_relation(self, part_ID: int, component_ID: int):
        new_relation = self.relation_repo.create_relation(
            part_ID=part_ID,
            component_ID=component_ID
        )
        return new_relation
    

    def service_get_relations_by_part_id(self, part_ID: int):
        relations = self.relation_repo.get_relations_by_part_id(part_ID=part_ID)
        return relations
    
    def service_delete_relation(self, relation_id: int):
        relation = self.relation_repo.get_relation_by_component_id(component_ID=relation_id)
        delete = self.relation_repo.delete_relation(relation=relation)
        return delete
    
    def service_get_all_relations(self):
        relations = self.relation_repo.get_all_relations()
        return relations
    
    def service_get_relation_by_component_id(self, component_ID: int):
        relation = self.relation_repo.get_relation_by_component_id(component_ID=component_ID)
        return relation