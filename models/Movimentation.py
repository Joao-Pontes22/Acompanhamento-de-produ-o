from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey, Date
from models.Models import base
from sqlalchemy.orm import relationship

class movimentations (base):
    __tablename__="movimentations"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    origin = Column("origin", String)
    employer_id = Column("employer_id", Integer)
    batch = Column("batch", String)
    qnty = Column("qnty", Integer)
    date = Column("date", Date)
    destination = Column("destination", String)

    def __init__(self, part_number,
                  batch, qnty, date,
                  destination, origin, employer_id):
        self.part_number = part_number
        self.batch = batch
        self.qnty = qnty
        self.date = date
        self.employer_id = employer_id
        self.origin = origin
        self.destination = destination