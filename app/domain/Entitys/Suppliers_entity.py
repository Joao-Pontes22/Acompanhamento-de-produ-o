# Entity for creating or updating a supplier
class  Suplliers_entity:
    def __init__(self, name:str, contact:str, phone:str, email:str ):
        if name is not None:
            self.name = name.upper()
        if contact is not None:
            self.contact = contact.upper()
        if phone is not None:
            self.phone = phone
        if email is not None:
            self.email = email.lower()