from app.models.Models import base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship


class Scraps (base):
    __tablename__="Scraps"

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