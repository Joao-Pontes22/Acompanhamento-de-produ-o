#FastAPI
from fastapi import APIRouter, Depends, HTTPException
#SQLAlchemy
from sqlalchemy.orm import Session
#Schemas
from app.Schemas.Queries.movimentation_query_params import MovimentationParameters
#Dependecies
from app.core.Dependecies import Init_Session
#Repository
from app.repositories.Movimentation_repository import MovimentationRepository
from app.repositories.PartAndComp_repository import PartsAndCompRepository
from app.repositories.Sectors_repository import SectorsRepository
from app.repositories.Employers_repository import EmployersRepository
#Service
from app.Services.Movimentation_Service import MovimentationService
#Exceptions
from app.domain.Exceptions import NotFoundException


Movimentaion_Router = APIRouter(prefix="/movimentation", tags=["Movimentation Operation"])


@Movimentaion_Router.get("/Get_all_movimentations",
                         response_model_exclude_none=True)
async def get_all_movimentations(session:Session = Depends(Init_Session)):

    repo = MovimentationRepository(session=session)
    service = MovimentationService(repo=repo)

    try:
        movimentations = service.get_all_movimentations()

        return movimentations
    
    except NotFoundException as e:
        raise HTTPException(message=str(e), status_code=404)
    

@Movimentaion_Router.get("/Get_filtered_movimentations")
async def get_filtered_movimentations(query_params: MovimentationParameters = Depends(),
                                     session:Session = Depends(Init_Session)
                                     ):
    
    
    
    parts_and_comp_repo = PartsAndCompRepository(session=session)
    sector_repo = SectorsRepository(session=session)
    emp_repo = EmployersRepository(session=session)
    repo = MovimentationRepository(session=session)
    service = MovimentationService(repo=repo,
                                   PartOrComp_Repo=parts_and_comp_repo,
                                   sector_repo=sector_repo,
                                   employer_repo=emp_repo)
    try:
        movimentations = service.get_filtred_movimentations(query_params=query_params)
        
        return movimentations
    
    except NotFoundException as e:
        raise HTTPException(detail=str(e), status_code=404)
    

@Movimentaion_Router.delete("/Delete_movimentation/{movimentation_id}")
async def delete_movimentation(movimentation_id: int, session:Session = Depends(Init_Session)):
    
    repo = MovimentationRepository(session=session)
    service = MovimentationService(repo=repo)

    try:
        deleted_movi = service.delete_movimentation(movimentation_id=movimentation_id)

        return {"message": "Movimentation deleted successfully"}
    
    except NotFoundException as e:
        raise HTTPException(detail=str(e), status_code=404)