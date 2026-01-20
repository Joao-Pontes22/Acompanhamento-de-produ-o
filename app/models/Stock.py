from app.models.Models import base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship


class Stock (base):
    __tablename__="Stock"
    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    sector_name = Column("sector_name", String, ForeignKey("Sectors.sector"))
    part_number = Column("part_number", String, ForeignKey("ComponentsAndParts.part_number"))
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