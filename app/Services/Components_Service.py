#Repository
from app.repositories.Components_repository import ComponentsRepository
from app.repositories.Suppliers_repository import SuppliersRepository
#Schema
from app.Schemas.Components_Schemas import ComponentsSchema, UpdateComponentsInfoSchema
#Entity
from app.domain.Entitys.Components_entitys import ComponentsEntity
from app.domain.Entitys.PartsAndComp_entitys import PartsAndCompsEntityFilter
#Exception
from app.domain.Exceptions import AlreadyExist, NotFoundException
#Value Object
from app.domain.Value_objects.Part_number import value_Part_number

class ComponentsService:
    def __init__(self, components_repo:ComponentsRepository):
        self.repo = components_repo

    
    def create_components(self, 
                          schema:ComponentsSchema, 
                          supplier_repo:SuppliersRepository
                        ):

        entity = ComponentsEntity(part_number=schema.part_number,
                                     description_material=schema.description,
                                     supplier_name=schema.supplier_name,
                                     cost=schema.cost,
                                     component_type=schema.component_type
                                     )
        component = self.repo.get_component_by_part_number(part_number=entity.part_number)
        if component:
            raise AlreadyExist(entity="component")
        
        supplier = supplier_repo.get_supplier_by_name(name=entity.supplier_name)
        if not supplier:
            raise NotFoundException(entity="Supplier")
        
        new_component = self.repo.create_component(part_number=entity.part_number,
                                                    description_material=entity.description_material,
                                                    supplier_name=entity.supplier_name,
                                                    cost=entity.cost,
                                                    component_type=entity.component_type)
        return new_component
    

    def get_all_component(self):

        component = self.repo.get_all_components()

        if not component:
            raise NotFoundException(entity="Components")
        
        return component

    def get_component_filtred(self, 
                                id:int = None, 
                                part_number:str = None, 
                                description:str = None, 
                                supplier:str = None, 
                                component_type:str = None
                                ):
        component_entity = PartsAndCompsEntityFilter(part_number=part_number, 
                                                     description=description, 
                                                     supplier=supplier, 
                                                     component_type=component_type
                                                     )
        
        components = self.repo.get_component_filtred(id=id, 
                                                    part_number=component_entity.part_number, 
                                                    description=component_entity.description, 
                                                    supplier=component_entity.supplier, 
                                                    component_type=component_entity.component_type)
        return components
    

    def update_component_info(self, 
                              part_number:str, 
                              schema:UpdateComponentsInfoSchema, 
                              supplier_repo:SuppliersRepository
                            ):
        
        value_part_number = value_Part_number(part_number=part_number)
        component = self.repo.get_component_by_part_number(part_number=value_part_number.part_number)
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
        
        value_part_number = value_Part_number(part_number=part_number)
        component = self.repo.get_component_by_part_number(part_number=value_part_number.part_number)
        if not component:
            raise NotFoundException(entity="Component")
        deleted = self.repo.delete_component(component=component)
        return deleted
    

    