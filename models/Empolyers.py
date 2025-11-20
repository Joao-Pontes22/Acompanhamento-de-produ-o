from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey, Date
from models.Models import base
from sqlalchemy.orm import relationship
# -------------------------------------------------------------------#

# Tabela de funcionários
# Employers table
class Employers (base):
    __tablename__="Employers"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    password = Column("password", String)
    sector = Column("sector", String)

    employer_sector = relationship("Sectors", back_populates="employers")

    def __init__(self, name, password, sector):
        self.name = name
        self.password = password
        self.sector = sector

    machiningproduction =  relationship("MachiningProduction", back_populates="machiningemployer")
    assemblyproduction = relationship("AssemblyProduction", back_populates="assemblyemployer")
