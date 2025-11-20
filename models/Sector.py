from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey, Date
from models.Models import base
from sqlalchemy.orm import relationship
# -------------------------------------------------------------------#

class Sectors (base):
    __tablename__ = "Sectors"


    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    sector = Column("sector", String)
    tag = Column("tag", String)
    employers = relationship("Employers", back_populates="employer_sector")

    def __init__(self, sector, tag):
      self.sector = sector
      self.tag = tag
