
class employers_entity:
    def __init__(self,name, sector, password, emp_id):
        if len(name) < 3:
            raise ValueError("Name has to be greather than 3 caracteres")
        
        if len(password) < 3:
            raise ValueError("Password has to be greather than 3 caacteres")
        
        self.name = name.upper()
        self.sector = sector.upper()
        self.password =password
        self.emp_id = emp_id