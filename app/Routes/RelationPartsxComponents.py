from fastapi import APIRouter, Depends
from app.Services.RelationPartsxComponents import RelationPartsxComponents_Services
from app.repositories.RelationPartsxComponents_repositorie import RelationPartsxComponents_repositorie
from sqlalchemy.orm import Session
from app.core.Dependecies import Init_Session
from app.models.Models import RelationPartsxComponents


PartsxComponents_Router = APIRouter(prefix="/parts_to_components", tags=["Parts to Components Relations"])



@PartsxComponents_Router.post("/create_relation")
async def create_relation(part_ID: int, component_ID: int, session:Session = Depends(Init_Session)):
    repo = RelationPartsxComponents_repositorie(session=session)
    service = RelationPartsxComponents_Services(relation_repo=repo)
    new_relation = service.service_create_relation(part_ID=part_ID, component_ID=component_ID)
    return new_relation




@PartsxComponents_Router.get("/relations_by_part/{part_ID}")
async def get_relations_by_part_id(part_ID:int, session:Session = Depends(Init_Session)):
    repo = RelationPartsxComponents_repositorie(session=session)
    service = RelationPartsxComponents_Services(relation_repo=repo)
    relations = service.service_get_relations_by_part_id(part_ID=part_ID)
    return relations




@PartsxComponents_Router.delete("/delete_relation/{relation_ID}")
async def delete_relation(relation_ID:int, session:Session = Depends(Init_Session)):
    repo = RelationPartsxComponents_repositorie(session=session)
    service = RelationPartsxComponents_Services(relation_repo=repo)
    delete = service.service_delete_relation(relation_id=relation_ID)
    return {"deleted": delete}



@PartsxComponents_Router.get("/all_relations")
async def get_all_relations(session:Session = Depends(Init_Session)):
    repo = RelationPartsxComponents_repositorie(session=session)
    service = RelationPartsxComponents_Services(relation_repo=repo)
    relations = service.service_get_all_relations()
    return relations