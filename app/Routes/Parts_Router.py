from fastapi import APIRouter, Depends, HTTPException
from app.core.Dependecies import Init_Session
from sqlalchemy.orm import Session
from app.Schemes.Parts_Schemes import Parts_Scheme, parts_Update_Scheme
from app.repositories.Parts_repositorie import Parts_Repositorie
from app.repositories.Clients_repositorie import Clients_repositorie
from app.Services.Parts_Services import Parts_Services

Part_Router = APIRouter(prefix="/Parts", tags=["Parts Operations"])
                

@Part_Router.post("/add_parts")
async def add_part(schemes: Parts_Scheme, session: Session = Depends(Init_Session)):
    repo = Parts_Repositorie(session=session)
    service = Parts_Services(parts_repo=repo)
    clients_repo = Clients_repositorie(session=session)
    new_part = service.service_create_Part(scheme=schemes,clients_repo=clients_repo)
    return {"message": "Part created successfuly",
            "PART":new_part}
    
@Part_Router.get("/get_parts", response_model=list[Parts_Scheme])
async def get_part(session: Session = Depends(Init_Session)):
    repo = Parts_Repositorie(session=session)
    service = Parts_Services(parts_repo=repo)
    return service.service_get_all_Parts()

@Part_Router.patch("/update_part/{id}")
async def update_part(id: int, scheme: parts_Update_Scheme, session: Session = Depends(Init_Session)):
    repo = Parts_Repositorie(session=session)
    clients_repo = Clients_repositorie(session=session)
    service = Parts_Services(parts_repo=repo)
    Updated_part = service.service_update_part_info(id=id, scheme=scheme, clients_repo=clients_repo)
    return {"message": "Parts updated successfuly",
            "Part": Updated_part}

@Part_Router.get("/Get_parts_by_id")
async def get_parts_by_id(id:int, session:Session = Depends(Init_Session)):
    repo = Parts_Repositorie(session=session)
    service = Parts_Services(parts_repo=repo)
    return service.service_get_part_by_id(id=id)

@Part_Router.get("/Get_parts_by_part_number")
async def get_parts_by_id(part_number:str, session:Session = Depends(Init_Session)):
    repo = Parts_Repositorie(session=session)
    service = Parts_Services(parts_repo=repo)
    return service.service_get_part_by_part_number(part_number=part_number)


@Part_Router.delete("/Delete_part")
async def delete_part(id:int, session:Session = Depends(Init_Session)):
    repo = Parts_Repositorie(session=session)
    service = Parts_Services(parts_repo=repo)
    deleted = service.service_delete_part(id=id)
    return {"message": "Part deleteded successful",
            "Part": deleted}

