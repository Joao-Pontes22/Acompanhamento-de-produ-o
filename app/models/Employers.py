
from app.models.Models import base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


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
    employer_sector = relationship("Sectors", back_populates="employers")
    machining_production =  relationship("MachiningProduction", back_populates="machining_employer")
    assembly_production = relationship("AssemblyProduction", back_populates="assembly_employer")
# -------------------------------------------------------------------#
    
    def __init__(self, name, password, sector_name, emp_id):
        self.name = name
        self.password = password
        self.sector_name = sector_name
        self.emp_id = emp_id