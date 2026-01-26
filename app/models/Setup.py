from app.models.Models import base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship


class Setup(base):
    __tablename__="Setup"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True )
    Machine = Column("Machine", String, ForeignKey("Machines.machine"))
    Part_number = Column("Part_number", String, ForeignKey("ComponentsAndParts.part_number"))
    Date = Column("Date", DateTime)
    Emp_id = Column("Emp_id", String, ForeignKey("Employers.emp_id"))
    Check_list = Column("Check_list", String, nullable=True)
    Notes = Column("Notes", String, nullable=True)
    Setup_time_minutes = Column("Setup_time_minutes", Integer, nullable=True)
    Status = Column("Status", String)

    machines = relationship("Machines", back_populates="setup")
    compandpart = relationship("ComponentsAndParts", back_populates="setup")
    employer = relationship("Employers", back_populates="setup")

    def __init__(self, 
                 Machine,
                 Part_number,
                 Date,
                 Check_list,
                 Notes,
                 Setup_time_minutes,
                 Status):
        
        self.Machine = Machine
        self.Part_number = Part_number
        self.Date = Date
        self.Check_list = Check_list
        self.Notes = Notes
        self.Setup_time_minutes = Setup_time_minutes
        self.Status = Status