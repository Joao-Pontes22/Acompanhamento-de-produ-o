from fastapi import HTTPException
from app.repositories.Parts_repository import PartsRepository
from app.repositories.Clients_repository import ClientsRepository
from app.Schemes.Parts_Schemes import PartsScheme, UpdatePartsInfoScheme
from app.domain.Entitys.Parts_entitys import PartsEntity
from app.domain.Entitys.PartsAndComp_entitys import PartsAndCompsEntity, PartsAndCompsEntityFilter
from app.domain.Exceptions import NotFoundException, AlreadyExist


class Parts_Services:
    def __init__(self, parts_repo:PartsRepository):
        self.repo = parts_repo



    def create_part(self, schema:PartsScheme, clients_repo:ClientsRepository):
        client = clients_repo.get_client_by_name(name=schema.client)
        if not client:
            raise NotFoundException(entity="Client")
        entity = PartsEntity(part_number=schema.part_number,
                             description_parts=schema.description,
                             client=schema.client,
                             cost=schema.cost
                             )
        part = self.repo.get_part_filtered_first(part_number=entity.part_number)
        if part:
            raise AlreadyExist(entity="Part")
        new_part = self.repo.create_part(part_number=entity.part_number,
                                         description=entity.description_parts,
                                         client=entity.client,
                                         cost=entity.cost
                                         )
        return new_part
    
    def get_all_parts(self):
        parts = self.repo.get_all_parts()
        if not parts:
            raise NotFoundException(entity="Part")
        return parts 
    
    def get_filtered_parts(self, 
                           id:int = None, 
                           part_number:str = None, 
                           description:str = None, 
                           client:str = None
                            ):
        entity = PartsAndCompsEntityFilter(part_number=part_number, 
                                           description=description, 
                                           client=client
                                            )
        parts = self.repo.get_parts_filtered(id=id, 
                                            part_number=entity.part_number, 
                                            description=entity.description, 
                                            client=entity.client
                                            )
        if not parts:
            raise NotFoundException(entity="Part")
        
        return parts
    
    def service_update_part_info(self, 
                                 part_number: str, 
                                 schema:UpdatePartsInfoScheme, 
                                 clients_repo:ClientsRepository
                                 ):
        
        part = self.repo.get_part_filtered_first(part_number=part_number)
        if not part:
            raise NotFoundException(entity="Part")
        
        entity = UpdatePartsInfoScheme(part_number=schema.part_number,
                             description_parts=schema.description,
                             client=schema.client,
                             cost=schema.cost
                            )
        if schema.client:
            client = clients_repo.get_client_by_name(name=schema.client)
            if not client:
                raise NotFoundException(entity="Client")
            
        for field, value, in schema.model_dump(exclude_unset=True).items():
            setattr(part, field, value )

        updated_info = self.repo.update_part_info(part=part)
        return updated_info

    def service_delete_part(self, part_number: str):
        part = self.repo.get_part_filtered_first(part_number=part_number)
        if not part:
            raise NotFoundException(entity="Part")
        deleted = self.repo.delete_part(part=part)
        return deleted                                                                                       