from app.models.Clients import Clients
# Repository for managing client data
class ClientsRepository:
    def __init__(self, session):
        self.session = session


    def create_client(self,
                      name: str,
                      contact: str,
                      phone: str,
                      email: str
                    ):
        
        new_client = Clients(name=name,
                             contact=contact,
                             phone=phone,
                             email=email
                            )
        self.session.add(new_client)
        self.session.commit()
        return new_client   
    

    def get_all_clients(self):
        clients = self.session.query(Clients).all()
        return clients
    
    def get_client_by_name(self, name):
        client = self.session.query(Clients).filter(Clients.name == name).first()
        return client


    def update_client(self, client):
        self.session.commit()
        self.session.refresh(client)
        return client

    def delete_client(self,client):
        self.session.delete(client)
        self.session.commit()
        return client
