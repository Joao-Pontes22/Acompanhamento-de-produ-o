from fastapi import APIRouter, Depends, HTTPException
from app.Services.RelationMachinedXRaw_Services import Service_RelationMachinedXRaw
from app.repositories.RelationMachinedxRaw_repositorie import RelationMachinedxRaw_repositorie
from app.repositories.Components_repositorie import Components_Repositorie
from sqlalchemy.orm import Session
from app.core.Dependecies import Init_Session
from app.Schemes.RelationMachinedXRaw_Schemes import RelationMachinedXRaw_Scheme
from app.domain.Exceptions import NotFoundException, AlreadyExist
RawToMachined_Router = APIRouter(prefix="/RelationMachinedXRaw", tags=["Raw to Machined Component Relations"])


@RawToMachined_Router.post("/add_relation")
async def create_relation(scheme:RelationMachinedXRaw_Scheme, session:Session = Depends(Init_Session)):
    repo = RelationMachinedxRaw_repositorie(session=session)
    comp_repo = Components_Repositorie(session=session)
    service = Service_RelationMachinedXRaw(repo=repo)
    try:
        new_relation = service.service_create_relation(scheme=scheme, comp_repo=comp_repo)
        return {"message": "Relation created successfuly"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AlreadyExist as e:
        raise HTTPException(status_code=409, detail=str(e))


@RawToMachined_Router.get("/get_relation_by_machined/{machined_ID}")
async def get_relation_by_machined_component(machined_ID:int, session:Session = Depends(Init_Session)):
    repo = RelationMachinedxRaw_repositorie(session=session)
    service = Service_RelationMachinedXRaw(repo=repo)
    try:
        relation = service.service_get_relation_by_machined_component(machined_component_ID=machined_ID)
        return relation
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@RawToMachined_Router.get("/get_relation_by_raw/{raw_ID}")
async def get_relation_by_raw_component(raw_ID:int, session:Session = Depends(Init_Session)):
    repo = RelationMachinedxRaw_repositorie(session=session)
    comp_repo = Components_Repositorie(session=session)
    service = Service_RelationMachinedXRaw(repo=repo)
    try:
        relation = service.service_get_relation_by_raw_component(raw_component_ID=raw_ID, comp_repo=comp_repo)
        return relation
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@RawToMachined_Router.delete("/delete_relation/{machined_component_id}")
async def delete_relation(machined_component_id:int, session:Session = Depends(Init_Session)):
    repo = RelationMachinedxRaw_repositorie(session=session)
    comp_repo = Components_Repositorie(session=session)
    service = Service_RelationMachinedXRaw(repo=repo)
    try:
        delete = service.service_delete_relation(machined_component_part_number=machined_component_id, comp_repo=comp_repo)
        return {"message": "Relation deleted successfuly"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@RawToMachined_Router.get("/get_all_relations")
async def get_all_relations(session:Session = Depends(Init_Session)):
    repo = RelationMachinedxRaw_repositorie(session=session)
    service = Service_RelationMachinedXRaw(repo=repo)
    try:
        relations = service.service_get_all_relations()
        return relations
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))