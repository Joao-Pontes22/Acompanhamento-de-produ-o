from fastapi import HTTPException
from app.repositories.Parts_repositorie import Parts_Repositorie
from app.repositories.Clients_repositorie import Clients_repositorie
from app.Schemes.Parts_Schemes import Parts_Scheme, parts_Update_Scheme
from app.domain.Entitys.Parts_entitys import Parts_entity
from app.domain.Entitys.PartsAndComp_entitys import PartsAndComp_entity, PartsAndComp_entity_filter
from app.domain.Value_objects.Part_number import value_Part_number
from app.domain.Exceptions import NotFoundException, AlreadyExist
from app.domain.Value_objects.Clients import value_Client


class Parts_Services:
    def __init__(self, parts_repo:Parts_Repositorie):
        self.repo = parts_repo



    def service_create_Part(self, scheme:Parts_Scheme, clients_repo:Clients_repositorie):
        client_value = value_Client(client=scheme.client)
        client = clients_repo.repo_find_clients_by_name(client_value.name)
        if not client:
            raise NotFoundException(entity="Customer")
        validated = Parts_entity(scheme=scheme)
        part = self.repo.repo_get_Parts_by_part_number(part_number=validated.part_number)
        if part:
            raise AlreadyExist(entity="Part")
        new_part = self.repo.repo_create_Part(scheme=validated)
        return new_part
    
    def service_get_all_Parts(self):
        Part = self.repo.repo_get_all_Parts()
        if not Part:
            raise NotFoundException(entity="Part")
        return Part 
    
    def service_get_filtered_parts(self, id:int = None, part_number:str = None, description:str = None, client:str = None):
        part_entity = PartsAndComp_entity_filter(part_number=part_number, description=description, client=client)
        parts = self.repo.repo_get_part_filteres(id=id, part_number=part_entity.part_number, description=part_entity.description, client=part_entity.client)
        if not parts:
            raise NotFoundException(entity="Part")
        return parts
    
    def service_update_part_info(self, part_number: str, scheme:parts_Update_Scheme, clients_repo:Clients_repositorie):
        part = self.repo.repo_get_part_filtered_first(part_number=part_number)
        if not part:
            raise NotFoundException(entity="Part")
        validated = Parts_entity(scheme=scheme)
        if scheme.client is not None:
            client = clients_repo.repo_find_clients_by_id(id=scheme.client)
            if not client:
                raise NotFoundException(entity="Customer")
            part.client = validated.client
        if scheme.part_number is not None:
            part.part_number = validated.part_number
        if scheme.description is not None:
            part.description = validated.description_parts
        if scheme.cost is not None:
            part.cost = validated.cost
        updated_info = self.repo.repo_update_Part_info(part=part)
        return updated_info

    def service_delete_part(self, part_number: str):
        part = self.repo.repo_get_part_filtered_first(part_number=part_number)
        if not part:
            raise NotFoundException(entity="Part")
        deleted = self.repo.repo_delete_part(part=part)
        return deleted                                                                                       