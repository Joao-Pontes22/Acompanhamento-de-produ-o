from app.models.Models import base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Machining_Production(base):
    __tablename__ = "Machining_Production"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    serial_ID = Column("serial_ID", Integer)
    sector_name = Column("sector_name", String, ForeignKey("Sectors.sector"))
    machine_name = Column("machine_name", String, ForeignKey("Machines.machine"))

    date = Column("date", DateTime)
    duration_process = Column("duration_process", DateTime)

    input_part_number = Column("input_part_number", String)
    output_part_number = Column("output_part_number", String)

    machining_batch = Column("machining_batch", String)
    assembly_batch = Column("assembly_batch", String)
    warehouse_batch = Column("warehouse_batch", String)

    emp_id_employer = Column("emp_id_employer", Integer, ForeignKey("Employers.emp_id"))
    status = Column("status", String)

    machining_employer = relationship("Employers", back_populates="machining_production")
    machine = relationship("Machines", back_populates="machining_production")
    sector = relationship("Sectors", back_populates="machining_production")

    def __init__(self, serial_ID, sector_name, date, input_part_number, output_part_number,
                 machining_batch, warehouse_batch, duration_process,
                 assembly_batch, emp_id_employer, status, machine_name):
        self.serial_ID = serial_ID
        self.sector_name = sector_name
        self.date = date
        self.input_part_number = input_part_number
        self.output_part_number = output_part_number
        self.machining_batch = machining_batch
        self.assembly_batch = assembly_batch
        self.warehouse_batch = warehouse_batch
        self.duration_process = duration_process
        self.emp_id_employer = emp_id_employer
        self.status = status
        self.machine_name = machine_name