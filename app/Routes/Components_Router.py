from fastapi import APIRouter, Depends, HTTPException
from app.core.Dependecies import Init_Session
from sqlalchemy.orm import Session
from app.Schemes.Components_Schemes import Components_Scheme, Components_Scheme_Update
from app.repositories.Components_repositorie import Components_Repositorie
from app.Services.Components_Services import Components_Services
from app.Schemes.Responses.Response_Components import Responde_Components
from app.repositories.Suppliers_repositorie import Suppliers_Repositorie
from app.domain.Exceptions import AlreadyExist, NotFoundException
Components_Router = APIRouter(prefix="/Components", tags=["Components Operations"])

@Components_Router.post("/add_component")
async def add_component(scheme: Components_Scheme,session: Session = Depends(Init_Session)):
    repo = Components_Repositorie(session=session)
    supllier_repo = Suppliers_Repositorie(session=session)
    service = Components_Services(components_repo=repo)
    try:
        new_component = service.service_create_components(scheme=scheme, supplier_repo=supllier_repo)
        return {"message": "Component created successful",
            "Component": new_component.part_number}
    except AlreadyExist as e:
        raise HTTPException(status_code=409, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@Components_Router.get("/Get_all_Components", response_model=list[Responde_Components])
async def get_components(session:Session=Depends(Init_Session)):
    repo = Components_Repositorie(session=session)
    service = Components_Services(components_repo=repo)
    try:
        components = service.service_get_all_component()
        return components
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))

@Components_Router.get("/get_components_filtered", response_model=list[Responde_Components])
async def get_components_filtered(id:int = None,part_number:str = None, description:str = None, supplier_ID:int = None, session:Session=Depends(Init_Session)):
    repo = Components_Repositorie(session=session)
    service = Components_Services(components_repo=repo)
    try:
        components = service.service_get_component_filteres(id=id,part_number=part_number, description=description, supplier_ID=supplier_ID)
        return components
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))

@Components_Router.patch("/update_component_info/{id}", response_model=Responde_Components)
async def update_component(id:int, scheme:Components_Scheme_Update, session:Session=Depends(Init_Session)):
    repo = Components_Repositorie(session=session)
    supllier_repo = Suppliers_Repositorie(session=session)
    service = Components_Services(components_repo=repo)
    try:
        updated_component = service.service_update_component_info(id=id, scheme=scheme, supplier_repo=supllier_repo)
        return updated_component
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@Components_Router.delete("/Delete_component/{id}")
async def delete_component(id:int, session:Session = Depends(Init_Session)):
    repo = Components_Repositorie(session=session)
    service = Components_Services(components_repo=repo)
    try:
        deleted_component = service.service_delete_component(id=id)
        return {"message": "Component deleted successfuly"}
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))

