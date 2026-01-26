#FastAPI
from fastapi import APIRouter, Depends, HTTPException

#SqlAlchemy
from sqlalchemy.orm import Session
#Dependecie
from app.core.Dependecies import Init_Session
#Exceptions
from app.domain.Exceptions import NotFoundException
#Repositorys
from app.repositories.Employers_repository import EmployersRepository
from app.repositories.Setup_repository import SetupRepository
from app.repositories.Machines_repository import MachineRepository
from app.repositories.PartAndComp_repository import PartsAndCompRepository
#Service
from app.Services.Setup_Service import SetupService
#Schema
from app.Schemas.Setup_Schema import SetupSchema
from app.Schemas.Queries.setup_query_params import SetupQueryParams


Setup_Router = APIRouter(prefix="/Setup", tags=["Setup operation"])


@Setup_Router.post("/create_setup")
async def create_setup(body:SetupSchema, session: Session = Depends(Init_Session) ):
    try: 
        repo = SetupRepository(session=session)
        employer_repo = EmployersRepository(session=session)
        machine_repo = MachineRepository(session=session)
        PartsorComp_repo = PartsAndCompRepository(session=session)
        service = SetupService(Setup_repo=repo)
        new_setup = service.create_setup(schema=body,
                                         machine_repo=machine_repo,
                                         partsorcomp_repo=PartsorComp_repo,
                                         employers_repo=employer_repo
                                         )
        return {"message": "Setup created successfuly"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@Setup_Router.get("/get_all_setups")
async def get_all_setups(session: Session = Depends(Init_Session) ):
    try:    
        repo = SetupRepository(session=session)
        service = SetupService(Setup_repo=repo)
        setups = service.get_all_setups()
        return setups
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    
@Setup_Router.get("/get_setup_filtered")
async def get_setup_filtered(query_params: SetupQueryParams = Depends(),
                             session: Session = Depends(Init_Session) ):
    try:
        repo = SetupRepository(session=session)
        service = SetupService(Setup_repo=repo)
        setups = service.get_setup_filtered(query_params=query_params)
        return setups
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))