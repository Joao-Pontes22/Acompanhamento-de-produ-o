from pydantic import BaseModel, ConfigDict
from datetime import date

class Machining_Production_Scheme(BaseModel):
    serial_ID : int
    sector_ID : int
    machine_ID : int

    Date : date
    duration_process : int

    input_part_number : str
    output_part_number : str

    machining_batch : str = None
    assembly_batch : str = None
    warehouse_batch : str = None

    emp_id_employer : int
    status : str


    model_config = ConfigDict(from_attributes=True)