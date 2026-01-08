
from app.models.Models import RelationPartsxComponents
from app.repositories.RelationPartsxComponents_repositorie import RelationPartsxComponents_repositorie
from app.repositories.Components_repositorie import Components_Repositorie
from app.domain.Exceptions import NotFoundException, AlreadyExist
class RelationPartsxComponents_Services:
    def __init__(self, relation_repo: RelationPartsxComponents_repositorie, component_repo=Components_Repositorie):
        self.relation_repo = relation_repo
        self.component_repo = component_repo


    def service_create_relation(self, part_ID: int, component_ID: int):
        component = self.component_repo.repo_get_Component_by_id(id=component_ID)
        if not component:
            raise NotFoundException("Component")
        relation = self.relation_repo.get_relation_by_component_id(component_ID=component_ID)
        if relation:
            raise AlreadyExist("Relation")
        new_relation = self.relation_repo.create_relation(
            part_ID=part_ID,
            component_ID=component_ID
        )
        return new_relation
    

    def service_get_relations_by_part_id(self, part_ID: int):
        relations = self.relation_repo.get_relations_by_part_id(part_ID=part_ID)
        if not relations:
            raise NotFoundException("Relations")
        return relations
    
    def service_delete_relation(self, relation_id: int):
        relation = self.relation_repo.get_relation_by_component_id(component_ID=relation_id)
        if not relation:
            raise NotFoundException("Relation")
        delete = self.relation_repo.delete_relation(relation=relation)
        return delete
    
    def service_get_all_relations(self):
        relations = self.relation_repo.get_all_relations()
        if not relations:
            raise NotFoundException("Relations")
        return relations
    
    def service_get_relation_by_component_id(self, component_ID: int):
        relation = self.relation_repo.get_relation_by_component_id(component_ID=component_ID)
        if not relation:
            raise NotFoundException("Relation")
        return relation