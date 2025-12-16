
class employers_entity:
    def __init__(self,name, sector_id, password):
        if len(name) < 3:
            raise ValueError("Name has to be greather than 3 caracteres")
        
        if len(password) < 3:
            raise ValueError("Password has to be greather than 3 caacteres")
        
        self.name = name.upper()
        self.sector_id = sector_id
        self.password =password