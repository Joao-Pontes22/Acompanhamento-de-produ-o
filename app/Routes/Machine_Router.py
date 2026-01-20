from fastapi import APIRouter, Depends, HTTPException
from app.core.Dependecies import Init_Session
from sqlalchemy.orm import Session
from app.Schemes.Machine_Schemes import Machine_Scheme, Update_Machine_Scheme
from app.repositories.Machines_repository import Machine_Repositorie
from app.repositories.Sectors_repository import Sectors_repositorie
from app.Services.Machine_services import Service_Machines
from app.domain.Exceptions import NotFoundException, AlreadyExist
from app.Schemes.Responses.Response_Machines import Response_Machines

Machine_Router = APIRouter(prefix="/Machine", tags=["Machines Operation"])


@Machine_Router.post("/POST_machine")
async def post_machine(scheme: Machine_Scheme, session: Session = Depends(Init_Session)):
    sectors_repo = Sectors_repositorie(session=session)
    machine_repo = Machine_Repositorie(session=session)
    service = Service_Machines(machine_repo=machine_repo)
    try:
        new_machine = service.service_create_machine(scheme=scheme, sectors_repo=sectors_repo)
        return {"message": "Machine created successfuly"}
    except AlreadyExist as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Machine_Router.get("/GET_machine", response_model=list[Response_Machines])
async def get_machines(session:Session = Depends(Init_Session)):
    repo = Machine_Repositorie(session=session)
    service = Service_Machines(machine_repo=repo)
    try:
        return service.service_get_all_machines()
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Machine_Router.get("/GET_machine_filtred", response_model=list[Response_Machines])
async def get_machines(id:int = None, machine:str = None, session:Session = Depends(Init_Session)):
    repo = Machine_Repositorie(session=session)
    service = Service_Machines(machine_repo=repo)
    try:
        return service.service_get_machine_filtred(id=id, machine=machine)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@Machine_Router.delete("/Delete_machine/{machine}")
async def delete_machine(machine:str, session:Session=Depends(Init_Session)):
    repo = Machine_Repositorie(session=session)
    service = Service_Machines(machine_repo=repo)
    try:
        return {"message": "Machine deleteded successfully",
                "Machine": service.service_delete_machine(machine=machine)}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Machine_Router.patch("/Update_machine/{machine}")
async def updatte_machine(machine:str, scheme:Update_Machine_Scheme, session:Session=Depends(Init_Session)):
    sectors_repo = Sectors_repositorie(session=session)
    repo = Machine_Repositorie(session=session)
    service = Service_Machines(machine_repo=repo)
    try:
        new_machines_info = service.service_update_machine_info(machine=machine, scheme=scheme, sectors_repo=sectors_repo)
        return {"message": "Machine updated successfully"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))