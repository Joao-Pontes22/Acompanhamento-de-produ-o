
# Entity for creating a new client
class ClientsEntity:
    def __init__(self,
                 name: str,
                 contact: str,
                 email: str,
                 phone: str): 

        self.name = name
        self.contact = contact
        self.email= email
        self.phone = phone

# Entity for updating client information
class UpdateClientsInfosEntity:
    def __init__(self,
                 name: str,
                 contact: str,
                 email: str,
                 phone: str):
        
        if name:
            self.name = name

        if contact:
            self.contact = contact 

        if email:
            self.email= email

        if phone:
            self.phone = phone