from pydantic import BaseModel, ConfigDict
from datetime import date

class Machining_Production_Scheme(BaseModel):
    sector_name : str
    machine_name : str
    Date : date
    duration_process : int
    input_part_number : str
    output_part_number : str
    batch : str
    emp_id_employer : str
    status : str
    model_config = ConfigDict(from_attributes=True)

class Machining_Production_filtred_Scheme(BaseModel):
    sector_name : str
    machine_name : str

    Date : date

    input_part_number : str
    output_part_number : str

    machining_batch : str = None
    batch : str = None

    emp_id_employer : str
    status : str


    model_config = ConfigDict(from_attributes=True)