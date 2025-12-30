from fastapi import APIRouter, Depends
from app.Services.RelationMachinedXRaw_Services import Service_RelationMachinedXRaw
from app.repositories.RelationMachinedxRaw_repositorie import RelationMachinedxRaw_repositorie
from app.repositories.Components_repositorie import Components_Repositorie
from sqlalchemy.orm import Session
from app.core.Dependecies import Init_Session
from app.Schemes.RelationMachinedXRaw_Schemes import RelationMachinedXRaw_Scheme

RawToMachined_Router = APIRouter(prefix="/raw_to_machined", tags=["Raw to Machined Component Relations"])
@RawToMachined_Router.post("/create_relation")


async def create_relation(scheme:RelationMachinedXRaw_Scheme, session:Session = Depends(Init_Session)):
    repo = RelationMachinedxRaw_repositorie(session=session)
    comp_repo = Components_Repositorie(session=session)
    service = Service_RelationMachinedXRaw(repo=repo)
    new_relation = service.service_create_relation(scheme=scheme, comp_repo=comp_repo)
    return new_relation


@RawToMachined_Router.get("/relation_by_machined/{machined_ID}")
async def get_relation_by_machined_component(machined_component_ID:int, session:Session = Depends(Init_Session)):
    repo = RelationMachinedxRaw_repositorie(session=session)
    service = Service_RelationMachinedXRaw(repo=repo)
    relation = service.service_get_relation_by_machined_component(machined_component_ID=machined_component_ID)
    return relation


@RawToMachined_Router.get("/relation_by_raw/{raw_ID}")
async def get_relation_by_raw_component(raw_component_ID:int, session:Session = Depends(Init_Session)):
    repo = RelationMachinedxRaw_repositorie(session=session)
    comp_repo = Components_Repositorie(session=session)
    service = Service_RelationMachinedXRaw(repo=repo)
    relation = service.service_get_relation_by_raw_component(raw_component_ID=raw_component_ID, comp_repo=comp_repo)
    return relation


@RawToMachined_Router.delete("/delete_relation/{machined_component_id}")
async def delete_relation(machined_component_id:int, session:Session = Depends(Init_Session)):
    repo = RelationMachinedxRaw_repositorie(session=session)
    comp_repo = Components_Repositorie(session=session)
    service = Service_RelationMachinedXRaw(repo=repo)
    delete = service.service_delete_relation(machined_component_id=machined_component_id, comp_repo=comp_repo)
    return {"deleted": delete}

@RawToMachined_Router.get("/all_relations")
async def get_all_relations(session:Session = Depends(Init_Session)):
    repo = RelationMachinedxRaw_repositorie(session=session)
    service = Service_RelationMachinedXRaw(repo=repo)
    relations = service.service_get_all_relations()
    return relations