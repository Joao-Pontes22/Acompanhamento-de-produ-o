from fastapi import HTTPException
from app.repositories.Parts_repositorie import Parts_Repositorie
from app.repositories.Clients_repositorie import Clients_repositorie
from app.Schemes.Parts_Schemes import Parts_Scheme, parts_Update_Scheme
from app.domain.Entitys.Parts_entitys import Parts_entity
from app.domain.Entitys.PartsAndComp_entitys import PartsAndComp_entity
from app.domain.Value_objects.Part_number import value_Part_number

class Parts_Services:
    def __init__(self, parts_repo:Parts_Repositorie):
        self.repo = parts_repo



    def service_create_Part(self, scheme:Parts_Scheme, clients_repo:Clients_repositorie):
        
        client = clients_repo.repo_find_clients_by_id(scheme.client_ID)
        if not client:
            raise HTTPException(status_code=400, detail="client not exist")
        if scheme.cost <=0:
            raise HTTPException(status_code=400, detail="Cost must be greater than zero")
        validated = Parts_entity(scheme=scheme)
        part = self.repo.repo_get_Parts_by_part_number(part_number=validated.part_number)
        if part:
            raise HTTPException(status_code=400, detail="Part already exist")
        new_component = self.repo.repo_create_Part(scheme=validated)
        return new_component
    
    def service_get_all_Parts(self):
        component = self.repo.repo_get_all_Parts()
        return component
    
    def service_get_part_by_part_number(self, part_number):
        value_part = value_Part_number(part_number=part_number)
        component = self.repo.repo_get_Parts_by_part_number(part_number=value_part.part_number)
        if not component:
            raise HTTPException(status_code=400, detail="Componnt not found")
        return component
    
    def service_get_part_by_id(self, id:int):
        component = self.repo.repo_get_Parts_by_id(id=id)
        if not component:
            raise HTTPException(status_code=400, detail="Componnt not found")
        return component
    
    def service_update_part_info(self, id:int, scheme:parts_Update_Scheme, clients_repo:Clients_repositorie):
        part = self.repo.repo_get_Parts_by_id(id=id)
        if not part:
            raise HTTPException(status_code=400, detail="Component not found")
        validated = Parts_entity(scheme=scheme)
        if scheme.client_ID is not None:
            client = clients_repo.repo_find_clients_by_id(id=scheme.client_ID)
            if not client:
                raise HTTPException(status_code=400, detail="Supllier not exist")
            part.client_ID = validated.client_ID
        if scheme.part_number is not None:
            part.part_number = validated.part_number
        if scheme.description is not None:
            part.description = validated.description_parts
        if scheme.cost is not None:
            if scheme.cost <= 0:
                raise HTTPException (status_code=400, detail="Cost bust be greater than zero")
            part.cost = validated.cost
        updated_info = self.repo.repo_update_Part_info(part=part)
        return updated_info

    def service_delete_part(self, id:int):
        part = self.repo.repo_get_Parts_by_id(id=id)
        if not part:
            raise HTTPException(status_code=400, detail="Component not found")
        deleted = self.repo.repo_delete_part(part=part)
        return deleted                                                                                       