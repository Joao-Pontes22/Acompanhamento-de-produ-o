from app.models.Models import base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

class movimentations (base):
    __tablename__="Movimentations"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    part_number = Column("part_number", String)
    origin = Column("origin", String)
    reason = Column("reason", String)
    movimentation_type = Column("movimentation_type", String)
    employer = Column("employer", Integer, ForeignKey("Employers.emp_id"))
    batch = Column("batch", String, nullable=True)
    machining_batch = Column("machining_batch", String, nullable=True)
    assembly_batch = Column("assembly_batch", String, nullable=True)
    qnty = Column("qnty", Integer)
    date = Column("date", Date)
    destination = Column("destination", String)

    def __init__(self, part_number,
                  batch, qnty, date,
                  destination, origin, employer, reason, movimentation_type, machining_batch, assembly_batch):
        self.part_number = part_number
        self.batch = batch
        self.qnty = qnty
        self.date = date
        self.employer = employer
        self.reason = reason
        self.movimentation_type = movimentation_type
        self.origin = origin
        self.destination = destination
        self.machining_batch = machining_batch
        self.assembly_batch = assembly_batch