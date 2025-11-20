from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey, Date
from models.Models import base
from sqlalchemy.orm import relationship
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
    supplier = Column("supplier", String)
    date_last_movimentation = Column("date_last_movimentation", Date)
    supplier_batch = Column("supplier_batch", String)
    race = Column("race", String)

    def __init__(self, part_number,
                  batch, qnty, entry_date, 
                  supplier, date_last_movimentation, 
                  supplier_batch, race):
        self.part_number = part_number
        self.batch = batch
        self.qnty = qnty
        self.entry_date = entry_date
        self.supplier = supplier
        self.date_last_movimentation = date_last_movimentation
        self.supplier_batch = supplier_batch
        self.race = race

# -------------------------------------------------------------------#

# Tabela de estoque da usinagem
# Machining stock table
class MachiningStock (base):
    __tablename__ = "MachiningStock"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String, ForeignKey("Components.ID"))
    batch = Column("batch", String)
    qnty = Column("qnty", Integer)
    entry_date = Column("entry_date", Date)
    supplier = Column("supplier", String)
    race = Column("race", String)

    components = relationship("Components", back_populates="machiningstock")
    def __init__(self, part_number,
                  batch, qnty, entry_date,
                  supplier, race):
        self.part_number = part_number
        self.batch = batch
        self.qnty = qnty
        self.entry_date = entry_date
        self.supplier = supplier
        self.race = race
