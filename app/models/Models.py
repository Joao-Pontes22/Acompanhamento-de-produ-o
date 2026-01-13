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
    sector_name = Column("sector_name", String, ForeignKey("Sectors.sector"))
# -------------------------------------------------------------------#
#Relacionamento
#Relationship
    sector = relationship("Sectors", back_populates="employers")
    employer_sector = relationship("Sectors", back_populates="employers")
    machining_production =  relationship("Machining_Production", back_populates="machining_employer")
    assembly_production = relationship("Assembly_Production", back_populates="assembly_employer")
# -------------------------------------------------------------------#
    
    def __init__(self, name, password, sector_name, emp_id):
        self.name = name
        self.password = password
        self.sector_name = sector_name
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
    machining_production = relationship("Machining_Production", back_populates="sector")
    def __init__(self, sector, tag):
      self.sector = sector
      self.tag = tag
# -------------------------------------------------------------------#

class Machines (base):
    __tablename__="Machines"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    machine = Column("machine", String)
    description_machine = Column("description_machine", String)
    sector_name = Column("sector_name", String, ForeignKey("Sectors.sector"))

    sector = relationship("Sectors", back_populates="machines")
    machining_production = relationship("Machining_Production", back_populates="machine")
    assembly_production = relationship("Assembly_Production", back_populates="machine")
    def __init__(self, machine, sector_name, description_machine):
        self.machine = machine
        self.sector_name = sector_name
        self.description_machine = description_machine
# -------------------------------------------------------------------#
# Tabela de produção da usinagem
# Machining production table

class Machining_Production(base):
    __tablename__ = "Machining_Production"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    serial_ID = Column("serial_ID", Integer)
    sector_name = Column("sector_name", String, ForeignKey("Sectors.sector"))
    machine_name = Column("machine_name", String, ForeignKey("Machines.machine"))

    date = Column("date", DateTime)
    duration_process = Column("duration_process", DateTime)

    input_part_number = Column("input_part_number", String)
    output_part_number = Column("output_part_number", String)

    machining_batch = Column("machining_batch", String)
    assembly_batch = Column("assembly_batch", String)
    warehouse_batch = Column("warehouse_batch", String)

    emp_id_employer = Column("emp_id_employer", Integer, ForeignKey("Employers.emp_id"))
    status = Column("status", String)

    machining_employer = relationship("Employers", back_populates="machining_production")
    machine = relationship("Machines", back_populates="machining_production")
    sector = relationship("Sectors", back_populates="machining_production")

    def __init__(self, serial_ID, sector_name, date, input_part_number, output_part_number,
                 machining_batch, warehouse_batch, duration_process,
                 assembly_batch, emp_id_employer, status, machine_name):
        self.serial_ID = serial_ID
        self.sector_name = sector_name
        self.date = date
        self.input_part_number = input_part_number
        self.output_part_number = output_part_number
        self.machining_batch = machining_batch
        self.assembly_batch = assembly_batch
        self.warehouse_batch = warehouse_batch
        self.duration_process = duration_process
        self.emp_id_employer = emp_id_employer
        self.status = status
        self.machine_name = machine_name
# -------------------------------------------------------------------#

class Assembly_Production (base):
    __tablename__="Assembly_Production"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    serial_ID = Column("serial_ID", Integer)
    machine_name = Column("machine_name", String, ForeignKey("Machines.machine"))
    date = Column("date", DateTime)
    duration_process = Column("duration_process", DateTime)
    input_part_number = Column("input_part_number", String)
    output_part_number = Column("output_part_number", String)
    assembly_batch = Column("assembly_batch", String)
    warehouse_batch = Column("warehouse_batch", String)
    emp_id_employer = Column("emp_id_employer", Integer, ForeignKey("Employers.emp_id"))
    status = Column("status", String)

    
    assembly_employer = relationship("Employers", back_populates="assembly_production")
    machine = relationship("Machines", back_populates="assembly_production")

    def __init__(self, serial_ID, machine_name, date, input_part_number, output_part_number,
                 assembly_batch, warehouse_batch, duration_process,
                 emp_id_employer, status):
        self.serial_ID = serial_ID
        self.machine_name = machine_name
        self.date = date
        self.input_part_number = input_part_number
        self.output_part_number = output_part_number
        self.assembly_batch = assembly_batch
        self.warehouse_batch = warehouse_batch
        self.duration_process = duration_process
        self.emp_id_employer = emp_id_employer
        self.status = status

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
    sector_name = Column("sector_name", String, ForeignKey("Sectors.sector"))
    part_number = Column("part_number", String, ForeignKey("components_and_parts.part_number"))
    batch = Column("batch", String, nullable=True)
    machining_batch = Column("machining_batch", String, nullable=True)
    machining_date = Column("machining_date", Date, nullable=True)
    assembly_batch = Column("assembly_batch", String, nullable=True)
    assembly_date = Column("assembly_date", Date, nullable=True)
    qnty = Column("qnty", Integer)
    entry_date = Column("entry_date", Date, nullable=True)
    supplier = Column("supplier", String, ForeignKey("Suppliers.name"), nullable=True)
    client = Column("client", String, ForeignKey("Clients.name"), nullable=True)
    status = Column("status", String)
    cost = Column("cost", String)

    sector = relationship("Sectors", back_populates="stock")
    suppliers = relationship("Suppliers", back_populates="stock")
    item = relationship("ComponentsAndParts", back_populates="stock")
    clients = relationship("Clients", back_populates="stock")
    def __init__(self, sector_name, part_number,
                 batch, machining_batch,
                 machining_date, 
                 assembly_batch, assembly_date,qnty,
                 entry_date,
                 supplier_name, status, cost, client_name):
        self.sector_name = sector_name
        self.part_number = part_number
        self.batch = batch
        self.machining_batch = machining_batch
        self.machining_date = machining_date
        self.qnty = qnty
        self.entry_date = entry_date
        self.supplier_name = supplier_name
        self.status = status
        self.cost = cost
        self.assembly_batch = assembly_batch
        self.assembly_date = assembly_date
        self.client_name = client_name
class movimentations (base):
    __tablename__="Movimentations"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    origin = Column("origin", String)
    reason = Column("reason", String)
    movimentation_type = Column("movimentation_type", String)
    employer_id = Column("employer_id", Integer, ForeignKey("Employers.emp_id"))
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
class Relation (base):
    __tablename__="Relation"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    create_item_Part_number = Column("create_item_Part_number", Integer)
    consume_item_Part_number = Column("consume_item_Part_number", Integer)
    qnty = Column("qnty", Integer)
   
    def __init__(self, create_item_Part_number, consume_item_Part_number, qnty):
        self.create_item_Part_number = create_item_Part_number
        self.consume_item_Part_number = consume_item_Part_number
        self.qnty = qnty

# -------------------------------------------------------------------#
class ComponentsAndParts(base):
    __tablename__ = "components_and_parts"

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

