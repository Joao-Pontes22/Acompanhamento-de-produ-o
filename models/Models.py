from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Date
import os

DATABASE_URL = "postgresql://finances_v7j8_user:5OqAIRw61E0lkEjF4aEitwwBpQyOwDoq@dpg-d49kqcq4d50c739cu690-a.virginia-postgres.render.com/finances_v7j8"
engine = create_engine(DATABASE_URL)
base = declarative_base()

# -------------------------------------------------------------------#
# Tabela de funcionários
# Employers table
class Employers (base):
    __tablename__="Employers"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    password = Column("password", String)
    sector_ID = Column("sector_ID",Integer, ForeignKey("Sectors.ID"))
# -------------------------------------------------------------------#
#Relacionamento
#Relationship
    
    employer_sector = relationship("Sectors", back_populates="employers")
    machining_production =  relationship("Machining_Production", back_populates="machining_employer")
    assembly_production = relationship("Assembly_Production", back_populates="assembly_employer")
# -------------------------------------------------------------------#
    
    def __init__(self, name, password, sector):
        self.name = name
        self.password = password
        self.sector_ID = sector
# -------------------------------------------------------------------#
# Tabela de setores
# Sectors table
class Sectors (base):
    __tablename__ = "Sectors"


    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    sector = Column("sector", String)
    tag = Column("tag", String)
    employers = relationship("Employers", back_populates="employer_sector")

    def __init__(self, sector, tag):
      self.sector = sector
      self.tag = tag
# -------------------------------------------------------------------#
# Tabela de produção da usinagem
# Machining production table

class Machining_Production (base):
    __tablename__ = "Machining_Production"

    serial_iD = Column("serial_ID", Integer, primary_key=True, autoincrement=True)
    date = Column("date", DateTime )
    part_number = Column("part_number", String)
    production_batch = Column("production_batch", String)
    employer = Column("employer", String)
    id_employer = Column("id_employer", Integer, ForeignKey("Employers.ID"))
    status = Column("status", String)

    machining_employer = relationship("Employers", back_populates="machining_production")
    assembly_production = relationship("Assembly_Production", back_populates="machining")

    def __init__(self, date, part_number,
                 production_batch, employer, id_employer, status):
        self.date = date
        self.part_number = part_number
        self.production_batch = production_batch
        self.employer = employer
        self.id_employer = id_employer
        self.status = status

class Assembly_Production (base):
    __tablename__="Assembly_Production"

    serial_ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    components_ID = Column("components_ID", Integer, ForeignKey("Machining_Production.serial_ID"))
    id_employer = Column("id_employer", Integer, ForeignKey("Employers.ID"))
    status = Column("status", String)
    initial_hour = Column("initial_hour", DateTime)
    final_hour = Column("final_hour", DateTime)
    machine = Column("machine", String)
    
    assembly_employer = relationship("Employers", back_populates="assembly_production")
    machining = relationship("Machining_Production", back_populates="assembly_production")

# -------------------------------------------------------------------#
# Tabela de sucatas
# Scraps table
class Scraps (base):
    __tablename__="Scraps"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    batch = Column("batch", String)
    qnty = Column("qnty", Integer)
    date = Column("date", Date)
    reason = Column("reason", String)

    def __init__(self, part_number,
                  batch, qnty, date,
                  reason):
        self.part_number = part_number
        self.batch = batch
        self.qnty = qnty
        self.date = date
        self.reason = reason

# -------------------------------------------------------------------#
# Tabela de estoque do warehouse
# Warehouse Stock table
class Warehouse (base):
    __tablename__="Warehouse"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    batch = Column("batch", String)
    qnty = Column("qnty", Integer)
    entry_date = Column("entry_date", Date)
    supplier_ID = Column("supplier_ID", Integer, ForeignKey("Suppliers.ID"))
    date_last_movimentation = Column("date_last_movimentation", Date)
    supplier_batch = Column("supplier_batch", String)
    race = Column("race", String)

    def __init__(self, part_number,
                  batch, qnty, entry_date, 
                  supplier_ID, date_last_movimentation, 
                  supplier_batch, race):
        self.part_number = part_number
        self.batch = batch
        self.qnty = qnty
        self.entry_date = entry_date
        self.supplier_ID = supplier_ID
        self.date_last_movimentation = date_last_movimentation
        self.supplier_batch = supplier_batch
        self.race = race

# -------------------------------------------------------------------#

# Tabela de estoque da usinagem
# Machining stock table
class MachiningStock (base):
    __tablename__ = "MachiningStock"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    batch = Column("batch", String)
    qnty = Column("qnty", Integer)
    entry_date = Column("entry_date", Date)
    supplier_ID = Column("supplier_ID", Integer, ForeignKey("Suppliers.ID"))
    race = Column("race", String)

    suppliers = relationship("Suppliers", back_populates="machiningstock")
    def __init__(self, part_number,
                  batch, qnty, entry_date,
                  supplier_ID, race):
        self.part_number = part_number
        self.batch = batch
        self.qnty = qnty
        self.entry_date = entry_date
        self.supplier_ID = supplier_ID
        self.race = race

class movimentations (base):
    __tablename__="Movimentations"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    origin = Column("origin", String)
    employer_id = Column("employer_id", Integer)
    batch = Column("batch", String)
    qnty = Column("qnty", Integer)
    date = Column("date", Date)
    destination = Column("destination", String)

    def __init__(self, part_number,
                  batch, qnty, date,
                  destination, origin, employer_id):
        self.part_number = part_number
        self.batch = batch
        self.qnty = qnty
        self.date = date
        self.employer_id = employer_id
        self.origin = origin
        self.destination = destination
# -------------------------------------------------------------------#
# Tabela de componentes
# Components table
class Components (base):
    __tablename__="Components"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    description_material = Column("description_material", String)
    supplier_ID =  Column("supplier_ID", ForeignKey("Suppliers.ID"))


#-------------------------------------------------------------------#
#Relacionamentos
#Relationships

    supplier =relationship("Suppliers", 
                            back_populates="rel_component")
    relationpartsxcomponents = relationship("RelationPartsxComponents",
                                             back_populates="components")

#-------------------------------------------------------------------#

    def __init__(self, part_number,
                description_material):
        
        self.part_number = part_number
        self.description_material = description_material

# -------------------------------------------------------------------#
# Tabela de peças
# Parts table

class Parts (base):
    __tablename__="Parts"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    description_parts = Column("description_parts", String)
    Clients_ID = Column("Clients_ID", Integer, ForeignKey("Clients.ID"))

    clients = relationship("Clients", back_populates="rel_parts")

    components_rel = relationship(
        "RelationPartsxComponents",
        back_populates="part"
    )

    def __init__(self, part_number, description_parts, Clients_ID):
        
        self.part_number = part_number
        self.Clients_ID = Clients_ID
        self.description_parts = description_parts

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
    machiningstock = relationship("MachiningStock", back_populates="suppliers")

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
