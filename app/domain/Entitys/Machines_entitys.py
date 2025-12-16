class Machine_Entity:
    def __init__(self, machine:str, sector_ID:int, description_Machine:str):
        if machine is not None:
            self.Machine = machine.upper()
        if sector_ID is not None:
            self.Sector_ID = sector_ID
        if description_Machine is not None:
            self.Description_Machine = description_Machine.lower()