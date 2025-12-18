from sqlalchemy .orm import Session
from app.models.Models import ComponentsAndParts
from app.domain.Entitys.Components_entitys import Components_entity
class Components_Repositorie:
    def __init__(self, session:Session):
        self.session = session


    def repo_create_Components(self, scheme:Components_entity):
        component = ComponentsAndParts(part_number=scheme.part_number,
                                   description=scheme.description_material,
                                   supplier_ID=scheme.supplier_ID,
                                   cost=scheme.cost,
                                   category="COMPONENT",
                                   client_ID=None)
       
        self.session.add(component)
        self.session.commit()
        return component
    
    def repo_get_all_Component(self):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.category == "COMPONENT").all()
    
    def repo_get_Component_by_id(self, id:int):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.id == id ).first()
    
    def repo_get_Component_by_part_number(self, part_number:str):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.part_number == part_number ).first()

    def repo_update_component_info(self, component:Components_Repositorie):
        self.session.commit()
        self.session.refresh(component)
        return component
    
    def repo_delete_component(self, component:Components_Repositorie):
        self.session.delete(component)
        self.session.commit()
        return(component)