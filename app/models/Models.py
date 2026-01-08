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
    emp_id = Column("emp_id", String, unique=True)
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
    
    def __init__(self, name, password, sector_ID, emp_id):
        self.name = name
        self.password = password
        self.sector_ID = sector_ID
        self.emp_id = emp_id
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
    description_machine = Column("description_machine", String)
    sector_ID = Column("sector_ID", Integer, ForeignKey("Sectors.ID"))

    sector = relationship("Sectors", back_populates="machines")
    machining_production = relationship("Machining_Production", back_populates="machine")

    def __init__(self, machine, sector_ID, description_machine):
        self.machine = machine
        self.sector_ID = sector_ID
        self.description_machine = description_machine
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
    part_number = Column("part_number", String, ForeignKey("components_and_parts.part_number"))
    batch = Column("batch", String, nullable=True)
    machining_batch = Column("machining_batch", String, nullable=True)
    machining_date = Column("machining_date", Date, nullable=True)
    assembly_batch = Column("assembly_batch", String, nullable=True)
    assembly_date = Column("assembly_date", Date, nullable=True)
    qnty = Column("qnty", Integer)
    entry_date = Column("entry_date", Date, nullable=True)
    supplier_ID = Column("supplier_ID", Integer, ForeignKey("Suppliers.ID"), nullable=True)
    client_ID = Column("client_ID", Integer, ForeignKey("Clients.ID"), nullable=True)
    status = Column("status", String)
    cost = Column("cost", String)

    sector = relationship("Sectors", back_populates="stock")
    suppliers = relationship("Suppliers", back_populates="stock")
    item = relationship("ComponentsAndParts", back_populates="stock")
    clients = relationship("Clients", back_populates="stock")
    def __init__(self, sector_ID, part_number,
                 batch, machining_batch,
                 machining_date, 
                 assembly_batch, assembly_date,qnty,
                 entry_date,
                 supplier_ID, status, cost, client_ID):
        self.sector_ID = sector_ID
        self.part_number = part_number
        self.batch = batch
        self.machining_batch = machining_batch
        self.machining_date = machining_date
        self.qnty = qnty
        self.entry_date = entry_date
        self.supplier_ID = supplier_ID
        self.status = status
        self.cost = cost
        self.assembly_batch = assembly_batch
        self.assembly_date = assembly_date
        self.client_ID = client_ID
class movimentations (base):
    __tablename__="Movimentations"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    origin = Column("origin", String)
    reason = Column("reason", String)
    movimentation_type = Column("movimentation_type", String)
    employer_id = Column("employer_id", Integer)
    batch = Column("batch", String, nullable=True)
    machining_batch = Column("machining_batch", String, nullable=True)
    assembly_batch = Column("assembly_batch", String, nullable=True)
    qnty = Column("qnty", Integer)
    date = Column("date", Date)
    destination = Column("destination", String)

    def __init__(self, part_number,
                  batch, qnty, date,
                  destination, origin, employer_id, reason, movimentation_type, machining_batch, assembly_batch):
        self.part_number = part_number
        self.batch = batch
        self.qnty = qnty
        self.date = date
        self.employer_id = employer_id
        self.reason = reason
        self.movimentation_type = movimentation_type
        self.origin = origin
        self.destination = destination
        self.machining_batch = machining_batch
        self.assembly_batch = assembly_batch
# ----------------------    ---------------------------------------------#
# Tabela de relação de peças com componentes
#
class RelationPartsxComponents (base):
    __tablename__="RelationPartsxComponents"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_ID = Column("part_ID", Integer, ForeignKey("components_and_parts.id"))
    components_ID = Column("components_ID", Integer, ForeignKey("components_and_parts.id"))
    qnty = Column("qnty", Integer)
    components = relationship("ComponentsAndParts", 
                              foreign_keys=[components_ID],
                              back_populates="parts_rel"
                              )
    part = relationship("ComponentsAndParts",
                        foreign_keys=[part_ID],
                        back_populates="comp_rel"
                        )
    def __init__(self, part_ID, components_ID, qnty):
        self.part_ID = part_ID
        self.components_ID = components_ID
        self.qnty = qnty
# -------------------------------------------------------------------#
class RelationMachinedxRaw (base):
    __tablename__="RelationMachinedxRaw"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    machined_ID = Column("machined_ID", Integer, ForeignKey("components_and_parts.id"))
    raw_ID = Column("raw_ID", Integer, ForeignKey("components_and_parts.id"))

    machined = relationship("ComponentsAndParts", 
                              foreign_keys=[machined_ID],
                              back_populates="raw_rel"
                              )
    raw = relationship("ComponentsAndParts",
                        foreign_keys=[raw_ID],
                        back_populates="machined_rel"
                        )
    def __init__(self, machined_ID, raw_ID, qnty):
        self.machined_ID = machined_ID
        self.raw_ID = raw_ID
        self.qnty = qnty
# -------------------------------------------------------------------#
class ComponentsAndParts(base):
    __tablename__ = "components_and_parts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    part_number = Column(String, unique=True, nullable=False)
    description = Column(String)
    category = Column(String, nullable=False)  
    client_ID = Column(Integer, ForeignKey("Clients.ID"), nullable=True)
    supplier_ID = Column(Integer, ForeignKey("Suppliers.ID"), nullable=True)
    cost = Column(Float)

    # Relacionamentos
    clients = relationship("Clients", back_populates="items")
    supplier = relationship("Suppliers", back_populates="items")
    stock = relationship("Stock", back_populates="item")
    parts_rel = relationship("RelationPartsxComponents",foreign_keys=[RelationPartsxComponents.part_ID], back_populates="part")
    comp_rel= relationship("RelationPartsxComponents",foreign_keys=[RelationPartsxComponents.components_ID],back_populates="components")
    raw_rel = relationship("RelationMachinedxRaw", foreign_keys=[RelationMachinedxRaw.raw_ID], back_populates="raw")
    machined_rel = relationship("RelationMachinedxRaw", foreign_keys=[RelationMachinedxRaw.machined_ID], back_populates="machined")

    def __init__(self, part_number, description, category, client_ID, supplier_ID,cost):
        self.part_number = part_number
        self.description = description
        self.category  = category
        self.client_ID=  client_ID
        self.supplier_ID = supplier_ID
        self.cost= cost




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

    items = relationship("ComponentsAndParts", back_populates="supplier")
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

    stock = relationship("Stock", back_populates="clients")
    items = relationship("ComponentsAndParts",  back_populates="clients")
    def __init__(self, name, contact, phone, email):
        self.name = name
        self.contact = contact
        self.phone = phone
        self.email = email

