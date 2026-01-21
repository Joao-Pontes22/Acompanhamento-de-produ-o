#FastAPI
from fastapi import APIRouter, Depends, HTTPException
#SQLAlchemy
from sqlalchemy.orm import Session
#Dependecies
from app.core.Dependecies import Init_Session
from app.core.Dependecies import Verify_Token
#Schemas e Responses
from app.Schemas.Stock_Schemas import StockSchema, StockTransferSchema, UpdateStockInfoSchema
from app.Schemas.Responses.Response_Stock import ResponseStock
#Repository
from app.repositories.Relation_repository import RelationRepository
from app.repositories.Stock_repository import StockRepository
from app.repositories.Components_repository import ComponentsRepository
from app.repositories.Parts_repository import PartsRepository
from app.repositories.Sectors_repository import SectorsRepository
from app.repositories.Movimentation_repository import MovimentationRepository
from app.repositories.PartAndComp_repository import PartsAndCompRepository
from app.repositories.Employers_repository import EmployersRepository
#Service
from app.Services.Stock_Service import StockService
from app.domain.Exceptions import NotFoundException




Stock_Router = APIRouter(prefix="/stock", tags=["Stock Operation"])


@Stock_Router.post("/Create_Stock")
async def create_stock(scheme:StockSchema,
                       session:Session = Depends(Init_Session), 
                       employer_id: int = Depends(Verify_Token)
                       ):
    
    stock_repo = StockRepository(session=session)
    sectors_repo = SectorsRepository(session=session)
    partsandcomp_repo = PartsAndCompRepository(session=session)
    relation_repo = RelationRepository(session=session)
    movimentation_repo = MovimentationRepository(session=session)
    employers_repo = EmployersRepository(session=session)
    service = StockService( repo=stock_repo, 
                            sectors_repo=sectors_repo, 
                            partsAndComp_repo=partsandcomp_repo, 
                            relation_repo=relation_repo, 
                            movimentation_repo=movimentation_repo, 
                            employers_repo=employers_repo)
    try:

        new_stock = service.create_stock(scheme=scheme, 
                                         employer_id=employer_id)

        return {"message": "Stock created successfully"}
    
    except NotFoundException as e:
        session.rollback()
        raise HTTPException(detail=str(e), status_code=404)

@Stock_Router.get("/Get_all_stock",
                   response_model=list[ResponseStock],
                   response_model_exclude_none=True
                   )
async def get_all_stock(session:Session = Depends(Init_Session)):
    stock_repo = StockRepository(session=session)
    service = StockService(repo=stock_repo)
    try:

        stock = service.get_all_stock()

        return stock
    
    except NotFoundException as e:
        session.rollback()
        raise HTTPException(detail=str(e), status_code=404)

@Stock_Router.get("/Get_filtered_stock")
async def get_filtered_stock(part_number:str = None,
                             status:str = None,
                             sector_name: str = None,
                             batch: str = None,
                             machining_batch: str = None,
                             assembly_batch: str = None,
                             session:Session = Depends(Init_Session)):
    
    stock_repo = StockRepository(session=session)
    service = StockService(repo=stock_repo)

    try:
        stock = service.get_filtred_stock(part_number=part_number, 
                                          status=status, 
                                          sector_name=sector_name
                                          )
        
        return stock
    
    except NotFoundException as e:
        session.rollback()
        raise HTTPException(detail=str(e), status_code=404)
    

@Stock_Router.delete("/Delete_stock/{stock_id}")
async def delete_stock(stock_id:int, 
                       session:Session = Depends(Init_Session)):
    
    stock_repo = StockRepository(session=session)
    service = StockService(repo=stock_repo)

    try:
        delete = service.delete_stock(stock_id=stock_id)

        return {"message": "Stock deleted successfully"}
    
    except NotFoundException as e:
        session.rollback()
        raise HTTPException(detail=str(e), status_code=404)
    

@Stock_Router.patch("/Transfer_stock/{stock_id}")
async def transfer_stock(scheme:StockTransferSchema, 
                         session:Session = Depends(Init_Session), 
                         employer_id: int = Depends(Verify_Token)
                         ):
    stock_repo = StockRepository(session=session)
    sectors_repo = SectorsRepository(session=session)
    partsandcomp_repo = PartsAndCompRepository(session=session)
    movimentation_repo = MovimentationRepository(session=session)
    employers_repo = EmployersRepository(session=session)
    service = StockService( repo=stock_repo, 
                            sectors_repo=sectors_repo, 
                            movimentation_repo=movimentation_repo, 
                            partsAndComp_repo=partsandcomp_repo,
                            employers_repo=employers_repo)
    try:

        transfered_stock = service.transfer_stock(scheme=scheme, employer_id=employer_id)

        return {"message": "Stock transferred successfully"}
    
    except NotFoundException as e:
        session.rollback()
        raise HTTPException(detail=str(e), status_code=404)
    
@Stock_Router.patch("/Update_stock/{stock_id}")
async def update_stock(stock_id:int, 
                       scheme:UpdateStockInfoSchema, 
                       session:Session = Depends(Init_Session)
                       ):
    
    stock_repo = StockRepository(session=session)
    service = StockService(repo=stock_repo)

    try:

        updated_stock = service.update_stock(stock_id=stock_id, 
                                             scheme=scheme)

        return {"message": "Stock updated successfully"}
    
    except NotFoundException as e:
        session.rollback()
        raise HTTPException(detail=str(e), status_code=404)
    except Exception as e:
        session.rollback()
        raise HTTPException(detail=str(e), status_code=500)