from sqlalchemy .orm import Session
from app.models.Models import Components
from app.Schemes.Components_Schemes import Components_Scheme, Components_Scheme_Update
class Components_Repositorie:
    def __init__(self, session:Session):
        self.session = session


    def repo_create_Components(self, scheme:Components_Scheme):
        new_component = Components(part_number=scheme.part_number,
                                   description_material=scheme.description_material,
                                   supplier_ID=scheme.supplier_ID,
                                   cost=scheme.cost)
        self.session.add(new_component)
        self.session.commit()
        return new_component
    
    def repo_get_all_Component(self):
        return self.session.query(Components).all()
    
    def repo_get_Component_by_id(self, id:int):
        return self.session.query(Components).filter(Components.ID == id ).first()
    
    def repo_get_Component_by_part_number(self, part_number:str):
        return self.session.query(Components).filter(Components.part_number == part_number ).first()

    def repo_update_component_info(self, component:Components_Repositorie):
        self.session.commit()
        self.session.refresh(component)
        return component
    
    def repo_delete_component(self, component:Components_Repositorie):
        self.session.delete(component)
        self.session.commit()
        return(component)