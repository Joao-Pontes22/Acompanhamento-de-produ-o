from sqlalchemy .orm import Session
from app.models.ComponentsAndParts import ComponentsAndParts
from app.domain.Entitys.Components_entitys import Components_entity
class Components_Repositorie:
    def __init__(self, session:Session):
        self.session = session


    def repo_create_Components(self, scheme:Components_entity):
        component = ComponentsAndParts(part_number=scheme.part_number,
                                   description=scheme.description_material,
                                   supplier_name=scheme.supplier,
                                   cost=scheme.cost,
                                   category="COMPONENT",
                                   client_name=None,
                                   component_type=scheme.component_type)
        self.session.add(component)
        self.session.commit()
        return component
    
    def repo_get_all_Component(self):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.category == "COMPONENT").all()
    
    def repo_get_Component_by_id(self, id:int):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.id == id ).first()
    
    def repo_get_Component_by_part_number(self, part_number:str):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.part_number == part_number ).first()
    
    
    def repo_get_raw_components(self, part_number:str):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.description.like("%bruto%"), ComponentsAndParts.part_number == part_number).first()


    def repo_get_machined_components(self, part_number:str):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.description.like("%usinado%"), ComponentsAndParts.part_number == part_number).first()
    
    
    def repo_update_component_info(self, component):
        self.session.commit()
        self.session.refresh(component)
        return component
    
    def repo_delete_component(self, component):
        self.session.delete(component)
        self.session.commit()
        return(component)
    

    def repo_get_component_filteres(self, id:int, part_number:str = None, description:str = None, supplier:str = None, component_type:str = None):
        query = self.session.query(ComponentsAndParts).filter(ComponentsAndParts.category == "COMPONENT")
        if id:
            query = query.filter(ComponentsAndParts.id ==id)
        if part_number:
            query = query.filter(ComponentsAndParts.part_number.like(f"%{part_number}%"))
        if description:
            query = query.filter(ComponentsAndParts.description.like(f"%{description}%"))
        if supplier:
            query = query.filter(ComponentsAndParts.supplier_name == supplier)
        if component_type:
            query = query.filter(ComponentsAndParts.component_type == component_type)
        return query.all()