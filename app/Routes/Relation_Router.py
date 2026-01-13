from fastapi import APIRouter, Depends, HTTPException
from app.Services.Relation_Services import RelationPartsxComponents_Services
from app.repositories.Components_repositorie import Components_Repositorie
from app.repositories.Relation_repositorie import Relation_repositorie
from sqlalchemy.orm import Session
from app.core.Dependecies import Init_Session
from app.domain.Exceptions import NotFoundException, AlreadyExist
from app.Schemes.Relation_Schemes import Relation_Scheme

PartsxComponents_Router = APIRouter(prefix="/relations", tags=["Parts to Components Relations"])



@PartsxComponents_Router.post("/create_relation")
async def create_relation(scheme: Relation_Scheme, session:Session = Depends(Init_Session)):
    repo = Relation_repositorie(session=session)
    component_repo = Components_Repositorie(session=session)
    service = RelationPartsxComponents_Services(relation_repo=repo, component_repo=component_repo)

    try:
        new_relation = service.service_create_relation(scheme=scheme)
        return {"message": "Relation created successfuly"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AlreadyExist as e:
        raise HTTPException(status_code=409, detail=str(e))




@PartsxComponents_Router.get("/relations_filtred")
async def get_relations_by_part_id(create_item_part_number: str = None, consume_item_part_number: str = None, id: int = None, session:Session = Depends(Init_Session)):
    repo = Relation_repositorie(session=session)
    service = RelationPartsxComponents_Services(relation_repo=repo)
    try:
        relations = service.service_get_relations_filtred(id=id, create_item_part_number=create_item_part_number, consume_item_part_number=consume_item_part_number)
        return relations
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))




@PartsxComponents_Router.delete("/delete_relation/{relation_ID}")
async def delete_relation( relation_ID: int, session:Session = Depends(Init_Session)):
    repo = Relation_repositorie(session=session)
    service = RelationPartsxComponents_Services(relation_repo=repo)
    try:
        delete = service.service_delete_relation(relation_id=relation_ID)
        return {"message": "Relation deleted successfuly"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@PartsxComponents_Router.get("/get_all_relations")
async def get_all_relations(session:Session = Depends(Init_Session)):
    repo = Relation_repositorie(session=session)
    service = RelationPartsxComponents_Services(relation_repo=repo)
    try:
        relations = service.service_get_all_relations()
        return relations
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))