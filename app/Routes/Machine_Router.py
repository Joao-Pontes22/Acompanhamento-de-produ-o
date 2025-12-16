from fastapi import APIRouter, Depends
from app.models.Models import Machines
from app.core.Dependecies import Init_Session
from sqlalchemy.orm import Session
from app.Schemes.Machine_Schemes import Machine_Scheme, Update_Machine_Scheme
from app.repositories.Machines_repositorie import Machine_Repositorie
from app.repositories.Sectors_repositorie import Sectors_repositorie
from app.Services.Machine_services import Service_Machines
Machine_Router = APIRouter(prefix="/Machine", tags=["Machines Operation"])



@Machine_Router.post("/POST_machine")
async def post_machine(scheme: Machine_Scheme, session: Session = Depends(Init_Session)):
    sectors_repo = Sectors_repositorie(session=session)
    machine_repo = Machine_Repositorie(session=session)
    service = Service_Machines(machine_repo=machine_repo)
    new_machine = service.service_create_machine(scheme=scheme, sectors_repo=sectors_repo)
    return {"message": "Machine created successfuly",
            "machine": new_machine}

@Machine_Router.get("/GET_machine")
async def get_machines(session:Session = Depends(Init_Session)):
    repo = Machine_Repositorie(session=session)
    service = Service_Machines(machine_repo=repo)
    return service.service_get_all_machines()

@Machine_Router.get("/GET_machine_by_id")
async def get_machines(id:int, session:Session = Depends(Init_Session)):
    repo = Machine_Repositorie(session=session)
    service = Service_Machines(machine_repo=repo)
    return service.service_get_machine_by_id(id=id)

@Machine_Router.get("/GET_machine_by_name")
async def get_machines(name:str, session:Session = Depends(Init_Session)):
    repo = Machine_Repositorie(session=session)
    service = Service_Machines(machine_repo=repo)
    return service.service_get_machine_by_name(name=name)

@Machine_Router.delete("/Delete_machine")
async def delete_machine(id:int, session:Session=Depends(Init_Session)):
    repo = Machine_Repositorie(session=session)
    service = Service_Machines(machine_repo=repo)
    return {"message": "Machine deleteded successfully",
            "Machine": service.service_delete_machine(id=id)}

@Machine_Router.patch("/Update_machine")
async def updatte_machine(id:int, scheme:Update_Machine_Scheme, session:Session=Depends(Init_Session)):
    sectors_repo = Sectors_repositorie(session=session)
    repo = Machine_Repositorie(session=session)
    service = Service_Machines(machine_repo=repo)
    return service.service_update_machine_info(id=id, scheme=scheme, sectors_repo=sectors_repo)