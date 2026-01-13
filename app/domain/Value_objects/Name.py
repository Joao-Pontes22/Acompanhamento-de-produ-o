


class value_Name:
    def __init__(self,name):
        if len(name) < 3:
            raise ValueError("Name has to be grather than 3 caracteres")
        self.name = name.upper()