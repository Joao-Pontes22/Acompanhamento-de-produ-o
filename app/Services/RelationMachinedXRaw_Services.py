from app.repositories.RelationMachinedxRaw_repositorie import RelationMachinedxRaw_repositorie
from app.Schemes.RelationMachinedXRaw_Schemes import RelationMachinedXRaw_Scheme
from app.repositories.Components_repositorie import Components_Repositorie
from app.domain.Exceptions import AlreadyExist, NotFoundException
class Service_RelationMachinedXRaw:
    def __init__(self, repo:RelationMachinedxRaw_repositorie):
        self.repo = repo

    def service_create_relation(self, scheme:RelationMachinedXRaw_Scheme, comp_repo:Components_Repositorie):
        component1 = comp_repo.repo_get_Component_by_id(id=scheme.raw_component_id)
        component2 = comp_repo.repo_get_Component_by_id(id=scheme.machined_component_id)
        relation = self.repo.get_relation_by_machined_id(machined_ID=scheme.machined_component_id)
        if relation:
            raise AlreadyExist("Relation")
        if not component1 or not component2:
            raise NotFoundException("Component")
        new_relation = self.repo.create_relation(scheme=scheme)
        return new_relation
    

    def service_get_relation_by_machined_component(self, machined_component_ID:int):
        relation = self.repo.get_relation_by_machined_id(machined_ID=machined_component_ID)
        if not relation:
            raise NotFoundException("Relation")
        return relation
    

    def service_get_relation_by_raw_component(self, raw_component_ID:int, comp_repo:Components_Repositorie):
        component = comp_repo.repo_get_Component_by_id(id=raw_component_ID)
        if not component:
            raise NotFoundException("Raw Component")
        relation = self.repo.get_relation_by_raw_ID(raw_ID=component.id)
        return relation
    

    def service_delete_relation(self, machined_component_part_number:str, comp_repo:Components_Repositorie):
        component = comp_repo.repo_get_Component_by_part_number(part_number=machined_component_part_number)
        if not component:
            raise NotFoundException("Machined Component")
        relation = self.repo.get_relation_by_machined_id(machined_ID=component.id)
        if not relation:
            raise NotFoundException("Relation")
        delete = self.repo.delete_relation(machined_component=relation)
        return delete
    

    def service_get_all_relations(self):
        relations = self.repo.get_all_relations()
        if not relations:
            raise NotFoundException("Relations")
        return relations