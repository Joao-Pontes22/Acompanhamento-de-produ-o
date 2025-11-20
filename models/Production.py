from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey, Date
from models.Models import base
from sqlalchemy.orm import relationship
# -------------------------------------------------------------------#
# Tabela de produção da usinagem
# Machining production table

class MachiningProduction (base):
    __tablename__ = "MachiningProduction"

    serial_iD = Column("Serial_ID", Integer, primary_key=True, autoincrement=True)
    date = Column("date", DateTime )
    part_number = Column("part_number", String)
    production_batch = Column("production_batch", String)
    employer = Column("employer", String)
    id_employer = Column("id_employer", Integer, ForeignKey("employers.ID"))
    status = Column("status", String)

    machiningemployer = relationship("Employers", back_populates="machiningproduction")

    def __init__(self, date, part_number,
                 production_batch, employer, id_employer, status):
        self.date = date
        self.part_number = part_number
        self.production_batch = production_batch
        self.employer = employer
        self.id_employer = id_employer
        self.status = status

class AssemblyProduction (base):
    __tablename__="AssemblyProduction"

    serial_ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    components_ID = Column("components_ID", Integer, ForeignKey("MachiningProduction.serial_ID"))

    assemblyemployer = relationship("Employers", back_populates="assemblyproduction")
# -------------------------------------------------------------------#
# Tabela de sucatas
# Scraps table
class scraps (base):
    __tablename__="scraps"

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
