from typing import Optional
class SetupEntity:
    def __init__(self, 
                 machine: str,
                 part_number: str,
                 date,
                 Emp_id: str,
                 Notes: Optional[str]
                 ):
        self.machine = machine
        self.part_number = part_number
        self.date = date
        self.Emp_id = Emp_id
        self.Notes = Notes if Notes else None
        
