#Schemas
from app.Schemas.Clients_Schemas import ClientsSchema, UpdateClientsInfoSchema
#Entity
from app.domain.Entitys.Clients_entitys import ClientsEntity
#Repository
from app.repositories.Clients_repository import ClientsRepository
#Exceptions
from app.domain.Exceptions import AlreadyExist, NotFoundException
#Value_Object
from app.domain.Value_objects.Clients import value_Client


class ClientsService:
    def __init__(self, repo:ClientsRepository):
        self.repo  = repo


    def create_client(self, schema:ClientsSchema):

        entity = ClientsEntity(name=schema.name,
                                         contact=schema.contact,
                                         email=schema.email,
                                         phone=schema.phone)
        client = self.repo.get_client_by_name(name=entity.name)
        if client:
            raise AlreadyExist(entity=entity.name)
        new_client = self.repo.create_client(name=entity.name,
                                                  contact=entity.contact,
                                                  phone=entity.phone,
                                                  email=entity.email
                                                  )
        return new_client
    
    def get_all_clients(self):
        clients = self.repo.get_all_clients()
        if not clients:
            raise NotFoundException(entity="Clients")
        return clients
    

    def get_by_name(self, name:str):
        value_client = value_Client(client=name)
        client = self.repo.get_client_by_name(name=value_client.name)
        if not client:
            raise NotFoundException(entity="Client")
        return client
    

    def update_client_info(self, name:str, schema:UpdateClientsInfoSchema):
        value_client = value_Client(client=name)
        client = self.repo.get_client_by_name(name=value_client.name)
        if not client:
            raise NotFoundException("Client")
        for field, value in schema.model_dump(exclude_unset=True).items():
            setattr(client, field, value)

        updated_client = self.repo.update_client(client=client)
        return updated_client
  

    def delete_client(self,name:str):
        value_client = value_Client(client=name)
        client = self.repo.get_client_by_name(name=value_client.name)
        if not client:
            raise NotFoundException(entity="Client")
        delete = self.repo.delete_client(client=client)
        return delete