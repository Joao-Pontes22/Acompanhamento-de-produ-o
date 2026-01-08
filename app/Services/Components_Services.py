from fastapi import HTTPException
from app.repositories.Components_repositorie import Components_Repositorie
from app.repositories.Suppliers_repositorie import Suppliers_Repositorie
from app.Schemes.Components_Schemes import Components_Scheme, Components_Scheme_Update
from app.domain.Entitys.Components_entitys import Components_entity
from app.domain.Entitys.PartsAndComp_entitys import PartsAndComp_entity
from app.domain.Value_objects.Part_number import value_Part_number
from app.domain.Exceptions import AlreadyExist, NotFoundException
class Components_Services:
    def __init__(self, components_repo:Components_Repositorie):
        self.repo = components_repo

    

    def service_create_components(self, scheme:Components_Scheme, supplier_repo:Suppliers_Repositorie):
        component = self.repo.repo_get_Component_by_part_number(part_number=scheme.part_number)
        if component:
            raise AlreadyExist(entity="component")
        supplier = supplier_repo.repo_get_suplier_by_id(scheme.supplier_ID)
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
     
    def service_update_component_info(self, id:int, scheme:Components_Scheme_Update, supplier_repo:Suppliers_Repositorie):
        component = self.repo.repo_get_Component_by_id(id=id)
        if not component:
            raise NotFoundException("Component")
        validated = Components_entity(scheme=scheme)
        if scheme.supplier_ID is not None:
            supplier = supplier_repo.repo_get_suplier_by_id(scheme.supplier_ID)
            if not supplier:
                raise NotFoundException("Supplier")
            component.supplier_ID = validated.supplier_ID
        if scheme.part_number is not None:
            component.part_number = validated.part_number
        if scheme.description is not None:
            component.description = validated.description_material
        if scheme.cost is not None:
            component.cost = validated.cost
        updated_info = self.repo.repo_update_component_info(component=component)
        return updated_info

    def service_delete_component(self, id:int):
        component = self.repo.repo_get_Component_by_id(id=id)
        if not component:
            raise NotFoundException(entity="Component")
        deleted = self.repo.repo_delete_component(component=component)
        return deleted
    

    def service_get_component_filteres(self, id:int, part_number:str = None, description:str = None, supplier_ID:int = None):
        components = self.repo.repo_get_component_filteres(id=id, part_number=part_number, description=description, supplier_ID=supplier_ID)
        return components