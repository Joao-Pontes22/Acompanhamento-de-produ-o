class Machine_Entity:
    def __init__(self, machine:str = None, sector:str = None, description_Machine:str = None):
        if machine is not None:
            self.Machine = machine.upper()
        if sector is not None:
            self.Sector = sector.upper()
        if description_Machine is not None:
            self.Description_Machine = description_Machine.lower()