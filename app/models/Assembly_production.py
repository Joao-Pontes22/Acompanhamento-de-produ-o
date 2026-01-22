from app.models.Models import base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class AssemblyProduction (base):
    __tablename__="AssemblyProduction"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    serial_ID = Column("serial_ID", Integer)
    machine_name = Column("machine_name", String, ForeignKey("Machines.machine"))
    date = Column("date", DateTime)
    duration_process = Column("duration_process", DateTime)
    input_part_number = Column("input_part_number", String)
    output_part_number = Column("output_part_number", String)
    assembly_batch = Column("assembly_batch", String)
    warehouse_batch = Column("warehouse_batch", String)
    emp_id_employer = Column("emp_id_employer", Integer, ForeignKey("Employers.emp_id"))
    status = Column("status", String)

    
    assembly_employer = relationship("Employers", back_populates="assembly_production")
    machine = relationship("Machines", back_populates="assembly_production")

    def __init__(self, serial_ID, machine_name, date, input_part_number, output_part_number,
                 assembly_batch, warehouse_batch, duration_process,
                 emp_id_employer, status):
        self.serial_ID = serial_ID
        self.machine_name = machine_name
        self.date = date
        self.input_part_number = input_part_number
        self.output_part_number = output_part_number
        self.assembly_batch = assembly_batch
        self.warehouse_batch = warehouse_batch
        self.duration_process = duration_process
        self.emp_id_employer = emp_id_employer
        self.status = status