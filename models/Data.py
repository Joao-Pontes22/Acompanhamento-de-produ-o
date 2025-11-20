from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey, Date
from models.Models import base
from sqlalchemy.orm import relationship

# -------------------------------------------------------------------#
# Tabela de componentes
# Components table
class Components (base):
    __tablename__="components"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    description_material = Column("description_material", String)
    supplier_ID =  Column("supplier_ID", ForeignKey("Suppliers.ID"))


    supplier =relationship("Suppliers", 
                            back_populates="rel_component")
    relationpartsxcomponents = relationship("RelationPartsxComponents",
                                             back_populates="components")

    def __init__(self, part_number,
                description_material):
        
        self.part_number = part_number
        self.description_material = description_material

# -------------------------------------------------------------------#
# Tabela de peças
# Parts table

class Parts (base):
    __tablename__="parts"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    Clients_ID = Column("Clients_ID", Integer, ForeignKey("Clients.ID"))

    clients = relationship("Clients", back_populates="rel_parts")

    components_rel = relationship(
        "RelationPartsxComponents",
        back_populates="part"
    )

    def __init__(self, part_number, Clients_ID):
        
        self.part_number = part_number
        self.Clients_ID = Clients_ID

# -------------------------------------------------------------------#
# Tabela de relação de peças com componentes
#
class RelationPartsxComponents (base):
    __tablename__="RelationPartsxComponents"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_ID = Column("part_ID", Integer, ForeignKey("Parts.ID"))
    components_ID = Column("components_ID", Integer, ForeignKey("Components.ID"))
    comp_qnty = Column("comp_qnty", Integer)

    components = relationship("Components", 
                              back_populates="relationpartsxcomponents"
                              )
    part = relationship("Parts",
                        back_populates="components_rel"
                        )

# Tabela de fornecedores
# Suppliers table

class Suppliers (base):
    __tablename__="Suppliers"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    contact = Column("contact", String)
    phone = Column("phone", String)
    email = Column("email", String)

    rel_component = relationship("Components", back_populates="supplier")

    def __init__(self, name, contact, phone, email):
        self.name = name
        self.contact = contact
        self.phone = phone
        self.email = email
# -------------------------------------------------------------------#
# Tabela de clientes
# Clients table

class Clients (base):
    __tablename__="Clients"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    contact = Column("contact", String)
    phone = Column("phone", String)
    email = Column("email", String)

    rel_parts = relationship("Parts",  back_populates="clients")
    def __init__(self, name, contact, phone, email):
        self.name = name
        self.contact = contact
        self.phone = phone
        self.email = email