from pydantic import BaseModel



class Components_Scheme(BaseModel):
    part_number : str
    description_material : str
    supplier_ID : int
    cost : float