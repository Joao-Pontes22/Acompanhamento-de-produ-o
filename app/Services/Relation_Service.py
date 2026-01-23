#Schema
from app.Schemas.Relation_Schemas import RelationSchema
from app.Schemas.Queries.relation_query_params import RelationParameters
#Repository
from app.repositories.Relation_repository import RelationRepository
from app.repositories.Components_repository import ComponentsRepository
#Excpetions
from app.domain.Exceptions import NotFoundException, AlreadyExist
#Entity
from app.domain.Entitys.Relation_entitys import RelationsEntity


class RelationServices:
    def __init__(self, relation_repo: RelationRepository, component_repo=ComponentsRepository):
        self.relation_repo = relation_repo
        self.component_repo = component_repo


    def create_relation(self, scheme:RelationSchema):

        relation_entity = RelationsEntity(create_item_part_number=scheme.create_item_part_number,
                                          consume_item_part_number=scheme.consume_item_part_number,
                                          qnty=1
                                          )
        
        component = self.component_repo.get_component_by_part_number(part_number=relation_entity.consume_item_part_number)
        if not component:
            raise NotFoundException("Component")
        
        relation = self.relation_repo.get_relations_filtred_first(consume_item_part_number=relation_entity.consume_item_part_number)
        if relation:
            raise AlreadyExist("Relation")
        
        new_relation = self.relation_repo.create_relation(create_item_part_number=relation_entity.create_item_part_number,
                                                          consume_item_part_number=relation_entity.consume_item_part_number,
                                                          qnty=relation_entity.qnty
                                                         )
        return new_relation
    

    def get_relations_filtred(self, 
                              query_params: RelationParameters):
        
        
        relations = self.relation_repo.get_relations_filtred(id=query_params.id, 
                                                             create_item_part_number=query_params.create_item_part_number, 
                                                             consume_item_part_number=query_params.consume_item_part_number
                                                             )
        if not relations:
            raise NotFoundException("Relations")
        
        return relations
    
    def delete_relation(self, relation_id: int):

        relation = self.relation_repo.get_relations_filtred_first(id=relation_id)
        if not relation:
            raise NotFoundException("Relation")
        
        delete = self.relation_repo.delete_relation(relation=relation)

        return delete
    
    def get_all_relations(self):

        relations = self.relation_repo.get_all_relations()

        if not relations:
            raise NotFoundException("Relations")
        return relations
    