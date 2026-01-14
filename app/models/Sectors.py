from app.models.Models import base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

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