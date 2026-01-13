from app.models.Models import Clients
from sqlalchemy.orm import Session
from app.core.Dependecies import Init_Session
from fastapi import HTTPException, Depends
from app.Schemes.Clients_Schemes import Clients_Scheme, Clients_Update_Scheme
from app.domain.Entitys.Clients_entitys import clients_entitys, update_clients_infos_entitys
from app.repositories.Clients_repositorie import Clients_repositorie
from app.domain.Exceptions import AlreadyExist, NotFoundException
from app.domain.Value_objects.Clients import value_Client

class Clients_Services:
    def __init__(self, repo:Clients_repositorie):
        self.repo  = repo

    
    def service_create_clients(self, scheme:Clients_Scheme):
        formated_infos = clients_entitys(name=scheme.name,
                                         contact=scheme.contact,
                                         email=scheme.email,
                                         phone=scheme.phone)
        client = self.repo.repo_find_clients_by_name(name=formated_infos.name)
        if client:
            raise AlreadyExist(entity=formated_infos.name)
        new_client = self.repo.repo_create_client(scheme=formated_infos)
        return new_client
    
    def service_get_all_clients(self):
        clients = self.repo.repo_find_all_clients()
        if not clients:
            raise NotFoundException(entity="Clients")
        return clients
    
    def service_get_by_name(self, name:str):
        client_entity = value_Client(client=name)
        client = self.repo.repo_find_clients_by_name(name=client_entity.name)
        if not client:
            raise NotFoundException(entity="Client")
        return client
    
    def update_client_info(self,name:str, scheme:Clients_Update_Scheme):
        client_entity = value_Client(client=name)
        client = self.repo.repo_find_clients_by_name(name=client_entity.name)
        if not client:
            raise NotFoundException("Client")
        
        validated = update_clients_infos_entitys(name=scheme.name,
                                                 contact=scheme.contact,
                                                 email=scheme.email,
                                                 phone=scheme.phone)
        if scheme.name is not None:
            client.name = validated.name

        if scheme.contact is not None:
            client.contact = validated.contact

        if scheme.email is not None:
            client.email = validated.email

        if scheme.phone is not None:
            client.phone = validated.phone

        updated_client = self.repo.repo_update_client(client=client)
        return updated_client
    
    def service_delete_client(self,name:str):
        client_entity = value_Client(client=name)
        Client = self.repo.repo_find_clients_by_name(name=client_entity.name)
        if not Client:
            raise NotFoundException(entity="Client")
        delete = self.repo.repo_delete_client(client=Client)
        return {"message": "Client deleted successfully"}