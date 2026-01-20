from app.repositories.Components_repository import ComponentsRepository
from app.repositories.Suppliers_repository import SuppliersRepository
from app.Schemes.Components_Schemes import ComponentsScheme, UpdateComponentsInfoScheme
from app.domain.Entitys.Components_entitys import ComponentsEntity
from app.domain.Entitys.PartsAndComp_entitys import PartsAndCompsEntityFilter
from app.domain.Exceptions import AlreadyExist, NotFoundException


class ComponentsServices:
    def __init__(self, components_repo:ComponentsRepository):
        self.repo = components_repo

    
    def create_components(self, 
                          scheme:ComponentsScheme, 
                          supplier_repo:SuppliersRepository
                        ):

        entity = ComponentsEntity(part_number=scheme.part_number,
                                     description_material=scheme.description,
                                     supplier_name=scheme.supplier_name,
                                     cost=scheme.cost,
                                     component_type=scheme.component_type
                                     )
        component = self.repo.get_component_by_part_number(part_number=entity.part_number)
        if component:
            raise AlreadyExist(entity="component")
        
        supplier = supplier_repo.get_supplier_by_name(name=entity.supplier_name)
        if not supplier:
            raise NotFoundException(entity="Supplier")
        
        new_component = self.repo.create_component(part_number=entity.part_number,
                                                         description_material=entity.description_material,
                                                         supplier_name=entity.supplier_name)
        return new_component
    
    def get_all_component(self):

        component = self.repo.get_all_components()

        if not component:
            raise NotFoundException(entity="Components")
        
        return component
     
    def update_component_info(self, 
                              part_number:str, 
                              schema:UpdateComponentsInfoScheme, 
                              supplier_repo:SuppliersRepository
                            ):
        
        component = self.repo.get_component_by_part_number(part_number=part_number)
        if not component:
            raise NotFoundException("Component")
        
        if schema.supplier_name:
            supplier = supplier_repo.get_supplier_by_name(schema.supplier_name)
            if not supplier:
                raise NotFoundException("Supplier")
        for field, value, in schema.model_dump(exclude_unset=True).items():
            setattr(component, field, value )

        updated_info = self.repo.update_component_info(component=component)
        return updated_info

    def delete_component(self, part_number:str):
        component = self.repo.get_component_by_part_number(part_number=part_number)
        if not component:
            raise NotFoundException(entity="Component")
        deleted = self.repo.delete_component(component=component)
        return deleted
    

    def service_get_component_filteres(self, 
                                       id:int, 
                                       part_number:str, 
                                       description:str, 
                                       supplier:str, 
                                       component_type:str
                                       ):
        component_entity = PartsAndCompsEntityFilter(part_number=part_number, 
                                                     description=description, 
                                                     supplier=supplier, 
                                                     component_type=component_type
                                                     )
        components = self.repo.get_component_filtered(id=id, 
                                                      part_number=component_entity.part_number, 
                                                      description=component_entity.description, 
                                                      supplier=component_entity.supplier, 
                                                      component_type=component_entity.component_type)
        return components