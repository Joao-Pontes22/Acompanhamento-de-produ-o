from fastapi import APIRouter, Depends, HTTPException
from app.core.Dependecies import Init_Session
from sqlalchemy.orm import Session
from app.Schemes.Components_Schemes import Components_Scheme, Components_Scheme_Update
from app.repositories.Components_repositorie import Components_Repositorie
from app.Services.Components_Services import Components_Services
from app.repositories.Suppliers_repositorie import Suppliers_Repositorie


Components_Router = APIRouter(prefix="/Components", tags=["Components Operations"])

@Components_Router.post("/add_component")
async def add_component(scheme: Components_Scheme,session: Session = Depends(Init_Session)):
    repo = Components_Repositorie(session=session)
    supllier_repo = Suppliers_Repositorie(session=session)
    service = Components_Services(components_repo=repo)
    new_component = service.service_create_components(scheme=scheme, supplier_repo=supllier_repo)
    return {"message": "Component created successful",
            "Component": new_component}

@Components_Router.get("/Get_Components")
async def get_components(session:Session=Depends(Init_Session)):
    repo = Components_Repositorie(session=session)
    service = Components_Services(components_repo=repo)
    components = service.service_get_all_component()
    return components

@Components_Router.get("/get_components_by_id")
async def get_components_by_id(id:int, session:Session=Depends(Init_Session)):
    repo = Components_Repositorie(session=session)
    service = Components_Services(components_repo=repo)
    components = service.service_get_componeent_by_id(id=id)
    return components

@Components_Router.get("/get_components_by_part_number")
async def get_components_by_pn(part_number:str, session:Session=Depends(Init_Session)):
    repo = Components_Repositorie(session=session)
    service = Components_Services(components_repo=repo)
    components = service.service_get_component_by_part_number(part_number=part_number)
    return components

@Components_Router.patch("/update_component_info")
async def update_component(id:int, scheme:Components_Scheme_Update, session:Session=Depends(Init_Session)):
    repo = Components_Repositorie(session=session)
    supllier_repo = Suppliers_Repositorie(session=session)
    service = Components_Services(components_repo=repo)
    updated_component = service.service_update_component_info(id=id, scheme=scheme, supplier_repo=supllier_repo)
    return updated_component

@Components_Router.delete("/Delete_component")
async def delete_component(id:int, session:Session = Depends(Init_Session)):
    repo = Components_Repositorie(session=session)
    service = Components_Services(components_repo=repo)
    deleted_component = service.service_delete_component(id=id)
    return {"message": "Component deleted successfuly",
            "Component": deleted_component}