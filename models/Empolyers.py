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
    sector_ID = Column(Integer, ForeignKey("Sectors.ID"))
# -------------------------------------------------------------------#
#Relacionamento
#Relationship
    
    employer_sector = relationship("Sectors", back_populates="employers")
    machiningproduction =  relationship("MachiningProduction", back_populates="machiningemployer")
    assemblyproduction = relationship("AssemblyProduction", back_populates="assemblyemployer")
# -------------------------------------------------------------------#
    
    def __init__(self, name, password, sector_ID):
        self.name = name
        self.password = password
        self.sector_ID = sector_ID

   
