from fastapi import HTTPException
from app.repositories.Components_repositorie import Components_Repositorie
from app.repositories.Suppliers_repositorie import Suppliers_Repositorie
from app.Schemes.Components_Schemes import Components_Scheme, Components_Scheme_Update
from app.domain.Entitys.Components_entitys import Components_entity
from app.domain.Entitys.PartsAndComp_entitys import PartsAndComp_entity, PartsAndComp_entity_filter
from app.domain.Value_objects.Part_number import value_Part_number
from app.domain.Exceptions import AlreadyExist, NotFoundException
from app.domain.Value_objects.Supplier import value_Supplier
class Components_Services:
    def __init__(self, components_repo:Components_Repositorie):
        self.repo = components_repo

    

    def service_create_components(self, scheme:Components_Scheme, supplier_repo:Suppliers_Repositorie):
        component = self.repo.repo_get_Component_by_part_number(part_number=scheme.part_number)
        if component:
            raise AlreadyExist(entity="component")
        supplier_entity = value_Supplier(supplier=scheme.supplier)
        supplier = supplier_repo.repo_get_supplier_by_name(supplier_entity.name)
        if not supplier:
            raise NotFoundException(entity="Supplier")
        validated = Components_entity(scheme=scheme)
        new_component = self.repo.repo_create_Components(scheme=validated)
        return new_component
    
    def service_get_all_component(self):
        component = self.repo.repo_get_all_Component()
        if not component:
            raise NotFoundException(entity="Components")
        return component
     
    def service_update_component_info(self, part_number:str, scheme:Components_Scheme_Update, supplier_repo:Suppliers_Repositorie):
        component = self.repo.repo_get_Component_by_part_number(part_number=part_number.upper())
        if not component:
            raise NotFoundException("Component")
        validated = Components_entity(scheme=scheme)
        if scheme.supplier is not None:
            supplier = supplier_repo.repo_get_supplier_by_name(validated.supplier)
            if not supplier:
                raise NotFoundException("Supplier")
            component.supplier_name = validated.supplier
        if scheme.part_number is not None:
            component.part_number = validated.part_number
        if scheme.description is not None:
            component.description = validated.description_material
        if scheme.cost is not None:
            component.cost = validated.cost
        if scheme.component_type is not None:
            component.component_type = validated.component_type
        updated_info = self.repo.repo_update_component_info(component=component)
        return updated_info

    def service_delete_component(self, part_number:str):
        component = self.repo.repo_get_Component_by_part_number(part_number=part_number.upper())
        if not component:
            raise NotFoundException(entity="Component")
        deleted = self.repo.repo_delete_component(component=component)
        return deleted
    

    def service_get_component_filteres(self, id:int, part_number:str = None, description:str = None, supplier:str = None, component_type:str = None):
        component_entity = PartsAndComp_entity_filter(part_number=part_number, description=description, supplier=supplier, component_type=component_type)
        components = self.repo.repo_get_component_filteres(id=id, part_number=component_entity.part_number, description=component_entity.description, supplier=component_entity.supplier, component_type=component_entity.component_type)
        return components