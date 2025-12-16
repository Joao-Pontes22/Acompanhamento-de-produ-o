
class clients_entitys:
    def __init__(self, name, contact, email, phone):
        self.name = name.upper()
        self.contact = contact.upper()
        self.email= email.lower()
        self.phone = phone

class update_clients_infos_entitys:
    def __init__(self, name=None, contact=None, email=None, phone=None):
        if name is not None:
            self.name = name.upper()
        if contact is  not None:
            self.contact = contact.upper()
        if email is not None:
            self.email= email.lower()
        if phone is not None:
            self.phone = phone