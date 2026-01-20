from app.Schemes.Machine_Schemes import MachineScheme

class MachineEntity:
    def __init__(self, 
                 machine_name: str,
                 sector_name: str,
                 description_machine: str 
                 ):
            self.machine_name = machine_name
            self.sector_name = sector_name
            self.description_machine = description_machine


class UpdateMachinesInfoEntity:
    def __init__(self,
                 machine_name: str,
                 sector_name: str,
                 description_machine: str 
                 ):
            
            if machine_name:
                self.machine_name = machine_name

            if sector_name:
                self.Sector_name = sector_name

            if description_machine:
                self.description_Machine = description_machine