
from app.Schemes.Relation_Schemes import Relation_Scheme
from app.repositories.Relation_repositorie import Relation_repositorie
from app.repositories.Components_repositorie import Components_Repositorie
from app.domain.Exceptions import NotFoundException, AlreadyExist
from app.domain.Entitys.Relation_entitys import Relation_Entity
from app.domain.Entitys.Relation_entitys import Relation_Entity_filtred
class RelationPartsxComponents_Services:
    def __init__(self, relation_repo: Relation_repositorie, component_repo=Components_Repositorie):
        self.relation_repo = relation_repo
        self.component_repo = component_repo


    def service_create_relation(self, scheme:Relation_Scheme):
        relation_entity = Relation_Entity(
            create_item_part_number=scheme.create_item_part_number,
            consume_item_part_number=scheme.consume_item_part_number,
            qnty=1
        )
        component = self.component_repo.repo_get_Component_by_part_number(part_number=relation_entity.consume_item_part_number)
        if not component:
            raise NotFoundException("Component")
        relation = self.relation_repo.get_relations_filtred_first(consume_item_part_number=relation_entity.consume_item_part_number)
        if relation:
            raise AlreadyExist("Relation")
        new_relation = self.relation_repo.create_relation(scheme=relation_entity
        )
        return new_relation
    

    def service_get_relations_filtred(self, id:int = None, create_item_part_number: str = None, consume_item_part_number: str = None):
        relation_entity = Relation_Entity_filtred(
            id=id,
            create_item_part_number=create_item_part_number,
            consume_item_part_number=consume_item_part_number
        )
        relations = self.relation_repo.get_relations_filtred(id=relation_entity.id, create_item_part_number=relation_entity.create_item_part_number, consume_item_part_number=relation_entity.consume_item_part_number)
        if not relations:
            raise NotFoundException("Relations")
        return relations
    
    def service_delete_relation(self, relation_id: int):
        relation = self.relation_repo.get_relations_filtred_first(id=relation_id)
        if not relation:
            raise NotFoundException("Relation")
        delete = self.relation_repo.delete_relation(relation=relation)
        return delete
    
    def service_get_all_relations(self):
        relations = self.relation_repo.get_all_relations()
        if not relations:
            raise NotFoundException("Relations")
        return relations
    