#FastAPI
from fastapi import APIRouter, Depends, HTTPException
#Service
from app.Services.Relation_Service import RelationServices
#Repository
from app.repositories.Components_repository import ComponentsRepository
from app.repositories.Relation_repository import RelationRepository
#SQLAlchemy
from sqlalchemy.orm import Session
#Dependecies
from app.core.Dependecies import Init_Session
#Exceptions
from app.domain.Exceptions import NotFoundException, AlreadyExist
#Schema
from app.Schemas.Relation_Schemas import RelationSchema


PartsxComponents_Router = APIRouter(prefix="/relations", tags=["Parts to Components Relations"])


@PartsxComponents_Router.post("/create_relation")
async def create_relation(scheme: RelationSchema, 
                          session:Session = Depends(Init_Session)):
    repo = RelationRepository(session=session)
    component_repo = ComponentsRepository(session=session)
    service = RelationRepository(relation_repo=repo, 
                                 component_repo=component_repo
                                 )

    try:
        new_relation = service.create_relation(scheme=scheme)

        return {"message": "Relation created successfuly"}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AlreadyExist as e:
        raise HTTPException(status_code=409, detail=str(e))




@PartsxComponents_Router.get("/relations_filtred")
async def get_relations_by_part_id(create_item_part_number: str = None, 
                                   consume_item_part_number: str = None, 
                                   id: int = None, 
                                   session:Session = Depends(Init_Session)
                                   ):
    
    repo = RelationRepository(session=session)
    service = RelationServices(relation_repo=repo)
    try:
        relations = service.get_relations_filtred(id=id, 
                                                  create_item_part_number=create_item_part_number, 
                                                  consume_item_part_number=consume_item_part_number
                                                  )
        
        return relations
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))




@PartsxComponents_Router.delete("/delete_relation/{relation_ID}")
async def delete_relation( relation_ID: int, 
                          session:Session = Depends(Init_Session)
                          ):
    
    repo = RelationRepository(session=session)
    service = RelationServices(relation_repo=repo)

    try:
        delete = service.delete_relation(relation_id=relation_ID)

        return {"message": "Relation deleted successfuly"}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@PartsxComponents_Router.get("/get_all_relations")
async def get_all_relations(session:Session = Depends(Init_Session)):

    repo = RelationRepository(session=session)
    service = RelationServices(relation_repo=repo)

    try:
        relations = service.get_all_relations()

        return relations
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))