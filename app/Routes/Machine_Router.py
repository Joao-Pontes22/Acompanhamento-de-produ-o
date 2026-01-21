#FastAPI
from fastapi import APIRouter, Depends, HTTPException
#Dependecies
from app.core.Dependecies import Init_Session
#SQLAlchemy
from sqlalchemy.orm import Session
#Schemas and responses
from app.Schemas.Machine_Schemas import MachineSchema, UpdateMachineInfoSchema
from app.Schemas.Responses.Response_Machines import ResponseMachines
#Repository
from app.repositories.Machines_repository import MachineRepository
from app.repositories.Sectors_repository import SectorsRepository

#Service
from app.Services.Machine_service import MachineService
#Exceptions
from app.domain.Exceptions import NotFoundException, AlreadyExist


Machine_Router = APIRouter(prefix="/Machine", tags=["Machines Operation"])


@Machine_Router.post("/POST_machine")
async def post_machine(scheme: MachineSchema, 
                       session: Session = Depends(Init_Session)
                       ):
    
    sectors_repo = SectorsRepository(session=session)
    machine_repo = MachineRepository(session=session)
    service = MachineService(machine_repo=machine_repo)

    try:

        new_machine = service.create_machine(scheme=scheme, sectors_repo=sectors_repo)

        return {"message": "Machine created successfuly"}
    
    except AlreadyExist as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@Machine_Router.get("/GET_machine", 
                    response_model=list[ResponseMachines])
async def get_machines(session:Session = Depends(Init_Session)):

    repo = MachineRepository(session=session)
    service = MachineService(machine_repo=repo)
    try:

        return service.get_all_machines()
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Machine_Router.get("/GET_machine_filtred", 
                    response_model=list[ResponseMachines]
                    )

async def get_machines(id:int = None, machine:str = None, session:Session = Depends(Init_Session)):
    
    repo = MachineRepository(session=session)
    service = MachineService(machine_repo=repo)
    try:

        return service.get_machine_filtred(id=id, machine=machine)
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@Machine_Router.delete("/Delete_machine/{machine}")
async def delete_machine(machine:str, 
                         session:Session=Depends(Init_Session)
                         ):
    
    repo = MachineRepository(session=session)
    service = MachineService(machine_repo=repo)
    
    try:
        delete = service.delete_machine(machine=machine)
        return {"message": "Machine deleteded successfully"}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Machine_Router.patch("/Update_machine/{machine}")
async def updatte_machine(machine:str, 
                          scheme:UpdateMachineInfoSchema, 
                          session:Session=Depends(Init_Session)
                          ):
    
    sectors_repo = SectorsRepository(session=session)
    repo = MachineRepository(session=session)
    service = MachineService(machine_repo=repo)

    try:
        new_machines_info = service.update_machine_info(machine=machine, 
                                                        scheme=scheme, 
                                                        sectors_repo=sectors_repo)
        
        return {"message": "Machine updated successfully"}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))