from app.models.Models import Clients
from app.Schemes.Clients_Schemes import Clients_Scheme, Clients_Update_Scheme

class Clients_repositorie:
    def __init__(self, session):
        self.session = session

    
    def repo_find_all_clients(self):
        clients = self.session.query(Clients).all()
        return clients
    
    def repo_find_clients_by_name(self, name):
        client = self.session.query(Clients).filter(Clients.name == name).first()
        return client

    def repo_find_clients_by_id(self,id):
        client = self.session.query(Clients).filter(Clients.ID == id).first()
        return client 
        
    def repo_create_client(self, scheme: Clients_Scheme):
        new_client = Clients(name=scheme.name,
                             contact=scheme.contact,
                             phone=scheme.phone,
                             email=scheme.email)
        self.session.add(new_client)
        self.session.commit()
        return new_client
    
    def repo_update_client(self, client:Clients_repositorie):
        self.session.commit()
        self.session.refresh(client)
        return client

    def repo_delete_client(self,client):
        self.session.delete(client)
        self.session.commit()
        return client
