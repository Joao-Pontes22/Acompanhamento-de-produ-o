from app.models.Models import base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship


class ComponentsAndParts(base):
    __tablename__ = "ComponentsAndParts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    part_number = Column(String, unique=True, nullable=False)
    description = Column(String)
    category = Column(String, nullable=False)  
    client_name = Column(String, ForeignKey("Clients.name"), nullable=True)
    supplier_name = Column(String, ForeignKey("Suppliers.name"), nullable=True)
    component_type = Column(String, nullable=True)
    cost = Column(Float)

    # Relacionamentos
    clients = relationship("Clients", back_populates="items")
    supplier = relationship("Suppliers", back_populates="items")
    stock = relationship("Stock", back_populates="item")
    

    def __init__(self, part_number, description, category, client_name, supplier_name,cost, component_type=None):
        self.part_number = part_number
        self.description = description
        self.category  = category
        self.client_name=  client_name
        self.supplier_name = supplier_name
        self.cost= cost
        self.component_type = component_type