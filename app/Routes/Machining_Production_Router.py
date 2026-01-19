from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.Dependecies import Init_Session
from app.Schemes.Machining_Production_Schemes import Machining_Production_Scheme
from app.repositories.Movimentation_repositorie import MovimentationRepository
from app.repositories.Relation_repositorie import Relation_repositorie
from app.repositories.Employers_repositories import employersRepo
from app.repositories.Machines_repositorie import Machine_Repositorie
from app.repositories.Sectors_repositorie import Sectors_repositorie
from app.repositories.Stock_repositorie import Stock_repositorie
from app.Services.Stock_Services import Stock_Services
from app.repositories.Machining_Production_repositorie import Machining_ProductionRepositorie
from app.Services.Machining_Production_Services import MachiningProductionServices
from app.domain.Exceptions import NotFoundException
from app.repositories.PartAndComp_repositorie import PartsAndComp_Repositorie

Machining_Production_Router = APIRouter(prefix="/machining_production", tags=["Machining Production Operation"])

@Machining_Production_Router.post("/Create_Machining_Production")
async def create_machining_production(scheme:Machining_Production_Scheme, session:Session = Depends(Init_Session)):
    repo = Machining_ProductionRepositorie(session=session)
    relation_repo = Relation_repositorie(session=session)
    sector_repo = Sectors_repositorie(session=session)
    machine_repo = Machine_Repositorie(session=session)
    employer_repo = employersRepo(session=session)
    stock_repo = Stock_repositorie(session=session)
    movimentation_repo = MovimentationRepository(session=session)
    partsandcomp_repo = PartsAndComp_Repositorie(session=session)
    service = MachiningProductionServices(Machining_Production_repo=repo)
    stock_service = Stock_Services(repo=stock_repo,
                                   sectors_repo=sector_repo,
                                    partsAndComp_repo=partsandcomp_repo)
    try:
        machining_production = service.service_create_machining_production(Scheme=scheme,
                                                                          relation_repo=relation_repo,
                                                                          sector_repo=sector_repo,
                                                                          machine_repo=machine_repo,
                                                                          employer_repo=employer_repo,
                                                                          stock_repo=stock_repo,
                                                                          movimentation_repo=movimentation_repo,
                                                                          stock_service=stock_service)
        return machining_production
    except NotFoundException as e:
        raise HTTPException(detail=str(e), status_code=404)