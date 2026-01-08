from app.domain.Exceptions import InvalidNameException
class clients_entitys:
    def __init__(self, name, contact, email, phone): 

        if len(name) <=3:
            raise InvalidNameException("Name must be grather than 3 caracteres")

        if len(contact) <3:
            raise InvalidNameException("Contact must be grather than 3 caracteres")
        self.name = name.upper()
        self.contact = contact.upper()
        self.email= email.lower()
        self.phone = phone

class update_clients_infos_entitys:
    def __init__(self, name=None, contact=None, email=None, phone=None):
        
        if name is not None:
            if len(name) <=3:
                raise InvalidNameException("Name must be grather than 3 caracteres")
            self.name = name.upper()
        if contact is  not None:
            if len(contact) <3:
                raise InvalidNameException("Contact must be grather than 3 caracteres")
            self.contact = contact.upper()   
        if email is not None:
            self.email= email.lower()
        if phone is not None:
            self.phone = phone