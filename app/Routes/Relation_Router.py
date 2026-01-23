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
#Schemas
from app.Schemas.Relation_Schemas import RelationSchema
from app.Schemas.Queries.relation_query_params import RelationParameters

PartsxComponents_Router = APIRouter(prefix="/Relations", tags=["Relations"])


@PartsxComponents_Router.post("/create_relation")
async def create_relation(body: RelationSchema, 
                          session:Session = Depends(Init_Session)):
    repo = RelationRepository(session=session)
    component_repo = ComponentsRepository(session=session)
    service = RelationRepository(relation_repo=repo, 
                                 component_repo=component_repo
                                 )

    try:
        new_relation = service.create_relation(scheme=body)

        return {"message": "Relation created successfuly"}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AlreadyExist as e:
        raise HTTPException(status_code=409, detail=str(e))




@PartsxComponents_Router.get("/relations_filtred")
async def get_relations_by_part_id(session:Session = Depends(Init_Session),
                                   query_params: RelationParameters = Depends(),):
    
    repo = RelationRepository(session=session)
    service = RelationServices(relation_repo=repo)
    try:
        relations = service.get_relations_filtred(query_params=query_params)
        
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