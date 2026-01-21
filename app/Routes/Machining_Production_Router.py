#FastAPI
from fastapi import APIRouter, Depends, HTTPException
#SQLAlchemy
from sqlalchemy.orm import Session
#Dependecies
from app.core.Dependecies import Init_Session
#Schemas
from app.Schemas.Machining_Production_Schemas import MachiningProductionSchema
#Repository
from app.repositories.Movimentation_repository import MovimentationRepository
from app.repositories.Relation_repository import RelationRepository
from app.repositories.Employers_repository import EmployersRepository
from app.repositories.Machines_repository import MachineRepository
from app.repositories.Sectors_repository import SectorsRepository
from app.repositories.Stock_repository import StockRepository
from app.repositories.Machining_Production_repository import Machining_ProductionRepository
from app.repositories.PartAndComp_repository import PartsAndCompRepository
#Service
from app.Services.Stock_Service import StockService
from app.Services.Machining_Production_Service import MachiningProductionServices
#Exceptions
from app.domain.Exceptions import NotFoundException


Machining_Production_Router = APIRouter(prefix="/machining_production", tags=["Machining Production Operation"])

@Machining_Production_Router.post("/Create_Machining_Production")
async def create_machining_production(scheme:MachiningProductionSchema, 
                                      session:Session = Depends(Init_Session)
                                      ):
    
    repo = Machining_ProductionRepository(session=session)
    relation_repo = RelationRepository(session=session)
    sector_repo = SectorsRepository(session=session)
    machine_repo = MachineRepository(session=session)
    employer_repo = EmployersRepository(session=session)
    stock_repo = StockRepository(session=session)
    movimentation_repo = MovimentationRepository(session=session)
    partsandcomp_repo = PartsAndCompRepository(session=session)

    service = MachiningProductionServices(Machining_Production_repo=repo)

    stock_service = StockService(repo=stock_repo,
                                 sectors_repo=sector_repo,
                                 partsAndComp_repo=partsandcomp_repo)
    try:
        machining_production = service.create_machining_production( Scheme=scheme,
                                                                    relation_repo=relation_repo,
                                                                    sector_repo=sector_repo,
                                                                    machine_repo=machine_repo,
                                                                    employer_repo=employer_repo,
                                                                    stock_repo=stock_repo,
                                                                    movimentation_repo=movimentation_repo,
                                                                    stock_service=stock_service
                                                                    )
        return machining_production
    
    except NotFoundException as e:
        raise HTTPException(detail=str(e), status_code=404)