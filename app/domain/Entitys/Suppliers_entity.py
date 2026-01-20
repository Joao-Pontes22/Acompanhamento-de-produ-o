# Entity for creating or updating a supplier
class  SuplliersEntity:
    def __init__(self, 
                 supplier_name:str, 
                 contact:str, 
                 phone:str, 
                 email:str ):
        self.supplier_name = supplier_name
        self.contact = contact
        self.phone = phone
        self.email = email

class  UpdateSuplliersInfoEntity:
    def __init__(self,
                 supplier_name:str, 
                 contact:str, 
                 phone:str, 
                 email:str ):
        if supplier_name:
            self.name = supplier_name
        if contact:
            self.contact = contact
        if phone:
            self.phone = phone
        if email:
            self.email = email