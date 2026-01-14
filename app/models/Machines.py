from app.models.Models import base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


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