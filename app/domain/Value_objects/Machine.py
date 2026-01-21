class ValueMachine:
    def __init__(self,machine):
        if len(machine) < 3:
            raise ValueError("machine has to be grather than 3 caracteres")
        self.machine = machine.upper()