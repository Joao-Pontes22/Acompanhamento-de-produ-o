

# Entity for creating a new employer
class EmployersEntity:
    def __init__(self,
                 name: str,
                 sector_name: str,
                 password: str,
                 emp_id: str
                 ):
      
        self.name = name
        self.sector_name = sector_name
        self.password = password
        self.emp_id =  emp_id
    