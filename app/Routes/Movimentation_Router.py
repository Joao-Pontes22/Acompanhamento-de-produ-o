from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.Dependecies import Init_Session
from app.domain.Exceptions import NotFoundException
from app.repositories.Movimentation_repository import MovimentationRepository
from app.repositories.Parts_repository import Parts_Repositorie
from app.repositories.Sectors_repository import Sectors_repositorie
from app.repositories.Components_repository import Components_Repositorie
from app.repositories.Employers_repository import employersRepo
from app.Services.Movimentation_Services import MovimentationService


Movimentaion_Router = APIRouter(prefix="/movimentation", tags=["Movimentation Operation"])


@Movimentaion_Router.get("/Get_all_movimentations",
                         response_model_exclude_none=True)
async def get_all_movimentations(session:Session = Depends(Init_Session)):
    repo = MovimentationRepository(session=session)
    service = MovimentationService(repo=repo)
    try:
        movimentations = service.service_get_all_movimentations()
        return movimentations
    except NotFoundException as e:
        raise HTTPException(message=str(e), status_code=404)
    

@Movimentaion_Router.get("/Get_filtered_movimentations")
async def get_filtered_movimentations(movimentation_id: int = None,
                                     part_number: str = None, 
                                     batch: str = None, 
                                     start_date = None, 
                                     end_date = None, 
                                     emp_id: int = None,
                                     movimentation_type: str = None, 
                                     origin: str = None,
                                     destination: str = None,
                                     machining_batch: str = None,
                                        assembly_batch: str = None,
                                     session:Session = Depends(Init_Session)):
    repo = MovimentationRepository(session=session)
    service = MovimentationService(repo=repo)
    parts_repo = Parts_Repositorie(session=session)
    components_repo = Components_Repositorie(session=session)
    sector_repo = Sectors_repositorie(session=session)
    emp_repo = employersRepo(session=session)
    try:
        movimentations = service.service_get_filtered_movimentations(movimentation_id=movimentation_id,
                                                                    part_number=part_number,
                                                                    batch=batch,
                                                                    start_date=start_date,
                                                                    end_date=end_date,
                                                                    emp_id=emp_id,
                                                                    movimentation_type=movimentation_type,
                                                                    origin=origin,
                                                                    destination=destination,
                                                                    machining_batch=machining_batch,
                                                                    assembly_batch=assembly_batch,
                                                                    components_repo=components_repo,
                                                                    parts_repo=parts_repo,
                                                                    sector_repo=sector_repo
                                                                    )
        return movimentations
    except NotFoundException as e:
        raise HTTPException(detail=str(e), status_code=404)
    

@Movimentaion_Router.delete("/Delete_movimentation/{movimentation_id}")
async def delete_movimentation(movimentation_id: int, session:Session = Depends(Init_Session)):
    repo = MovimentationRepository(session=session)
    service = MovimentationService(repo=repo)
    try:
        deleted_movi = service.service_delete_movimentation(movimentation_id=movimentation_id)
        return {"message": "Movimentation deleted successfully",
                "Deleted_Movimentation": deleted_movi }
    except NotFoundException as e:
        raise HTTPException(detail=str(e), status_code=404)