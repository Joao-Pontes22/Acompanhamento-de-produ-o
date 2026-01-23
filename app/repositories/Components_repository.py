from sqlalchemy .orm import Session
from app.models.ComponentsAndParts import ComponentsAndParts
from typing import Optional
# Repository for managing component data
class ComponentsRepository:
    def __init__(self, session:Session):
        self.session = session

# Methods for CRUD operations on components
    def create_component(self, 
                               part_number: str,
                               description_material: str,
                               supplier_name: str,
                               cost: float,
                               component_type: str
                               ):
        component = ComponentsAndParts(part_number=part_number,
                                   description=description_material,
                                   supplier_name=supplier_name,
                                   cost=cost,
                                   category="COMPONENT",
                                   client_name=None,
                                   component_type=component_type)
        self.session.add(component)
        self.session.commit()
        return component
    
    def get_all_components(self):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.category == "COMPONENT").all()
    
    def get_component_by_id(self, id:int):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.id == id ).first()
    
    def get_component_by_part_number(self, part_number:str):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.part_number == part_number ).first()

    
    def update_component_info(self, component):
        self.session.commit()
        self.session.refresh(component)
        return component
    
    def delete_component(self, component):
        self.session.delete(component)
        self.session.commit()
        return(component)
    

    def get_component_filtred(self, 
                                    id: Optional[int] = None, 
                                    part_number: Optional[str] = None, 
                                    description: Optional[str] = None, 
                                    supplier: Optional[str] = None, 
                                    component_type: Optional[str] = None
                                    ):
        
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