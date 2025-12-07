from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Date
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
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
    stock = relationship("Stock", back_populates="sector")
    machines = relationship("Machines", back_populates="sector")
    def __init__(self, sector, tag):
      self.sector = sector
      self.tag = tag
# -------------------------------------------------------------------#

class Machines (base):
    __tablename__="Machines"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    machine = Column("machine", String)
    sector_ID = Column("sector_ID", Integer, ForeignKey("Sectors.ID"))

    sector = relationship("Sectors", back_populates="machines")
    machining_production = relationship("Machining_Production", back_populates="machine")

    def __init__(self, machine, sector_ID):
        self.machine = machine
        self.sector_ID = sector_ID
# -------------------------------------------------------------------#
# Tabela de produção da usinagem
# Machining production table

class Machining_Production (base):
    __tablename__ = "Machining_Production"

    serial_iD = Column("serial_ID", Integer, primary_key=True, autoincrement=True)
    sector_ID = Column("sector_ID", Integer, ForeignKey("Sectors.ID"))
    machine_ID = Column("machine_ID", Integer, ForeignKey("Machines.ID"))
    date = Column("date", DateTime )
    initial_hour = Column("initial_hour", DateTime)
    final_hour = Column("final_hour", DateTime)
    part_number = Column("part_number", String)
    production_batch = Column("production_batch", String)
    warehouse_batch = Column("warehouse_batch", String)
    employer = Column("employer", String)
    id_employer = Column("id_employer", Integer, ForeignKey("Employers.ID"))
    status = Column("status", String)

    machining_employer = relationship("Employers", back_populates="machining_production")
    assembly_production = relationship("Assembly_Production", back_populates="machining")
    machine = relationship("Machines", back_populates="machining_production")
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
class Stock (base):
    __tablename__="Stock"
    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    sector_ID = Column("sector_ID", Integer, ForeignKey("Sectors.ID"))
    part_number = Column("part_number", String, ForeignKey("componentsAndparts.part_number"))
    warehouse_batch = Column("warehouse_batch", String)
    machining_batch = Column("machining_batch", String)
    machining_date = Column("machining_date", Date)
    qnty = Column("qnty", Integer)
    entry_date_warehouse_batch = Column("entry_date_warehouse_batch", Date)
    supplier_ID = Column("supplier_ID", Integer, ForeignKey("Suppliers.ID"))
    status = Column("status", String)
    cost = Column("cost", String)

    sector = relationship("Sectors", back_populates="stock")
    suppliers = relationship("Suppliers", back_populates="stock")
    componentsAndparts = relationship("componentsAndparts", back_populates="stock")
    def __init__(self, sector_ID, part_number,
                 warehouse_batch, machining_batch,
                 machining_date, qnty,
                 entry_date_warehouse_batch,
                 supplier_ID, status, cost):
        self.sector_ID = sector_ID
        self.part_number = part_number
        self.warehouse_batch = warehouse_batch
        self.machining_batch = machining_batch
        self.machining_date = machining_date
        self.qnty = qnty
        self.entry_date_warehouse_batch = entry_date_warehouse_batch
        self.supplier_ID = supplier_ID
        self.status = status
        self.cost = cost

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
    supplier_ID =  Column("supplier_ID", Integer, ForeignKey("Suppliers.ID"))
    cost = Column("cost", Float)
    supplier =relationship("Suppliers", 
                            back_populates="rel_component")
    relationpartsxcomponents = relationship("RelationPartsxComponents",
                                             back_populates="components")

    def __init__(self, part_number,
                description_material,supplier_ID, cost):
        
        self.part_number = part_number
        self.description_material = description_material
        self.supplier_ID = supplier_ID
        self.cost = cost

# -------------------------------------------------------------------#
# Tabela de peças
# Parts table

class Parts (base):
    __tablename__="Parts"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    description_parts = Column("description_parts", String)
    clients_ID = Column("Clients_ID", Integer, ForeignKey("Clients.ID"))
    cost = Column("cost", Float)

    clients = relationship("Clients", back_populates="rel_parts")

    components_rel = relationship(
        "RelationPartsxComponents",
        back_populates="part"
    )

    def __init__(self, part_number, description_parts, clients_ID, cost):
        
        self.part_number = part_number
        self.clients_ID = clients_ID
        self.description_parts = description_parts
        self.cost = cost

# -------------------------------------------------------------------#
# Tabela de relação de peças com componentes
#
class RelationPartsxComponents (base):
    __tablename__="RelationPartsxComponents"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_ID = Column("part_ID", Integer, ForeignKey("Parts.ID"))
    components_ID = Column("components_ID", Integer, ForeignKey("Components.ID"))

    components = relationship("Components", 
                              back_populates="relationpartsxcomponents"
                              )
    part = relationship("Parts",
                        back_populates="components_rel"
                        )
    def __init__(self, part_ID, components_ID):
        self.part_ID = part_ID
        self.components_ID = components_ID

class componentsAndparts (base):
    __tablename__="componentsAndparts"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    description = Column("description", String)
    category = Column("category", String)
    stock = relationship("Stock", back_populates="componentsAndparts")
    cost = Column("cost", Float)
    def __init__(self, part_number, description, category, cost):
        self.part_number = part_number
        self.description = description
        self.category = category 




# -------------------------------------------------------------------#
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
    stock = relationship("Stock", back_populates="suppliers")

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

create_all = base.metadata.create_all(engine)
