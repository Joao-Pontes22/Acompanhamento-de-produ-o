class value_Part_number:
    def __init__(self,part_number):
        if len(part_number) < 3:
            raise ValueError("Part_number has to be grather than 3 carracteres")
        self.part_number = part_number.upper()