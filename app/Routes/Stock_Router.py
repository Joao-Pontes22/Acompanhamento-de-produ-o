from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.Dependecies import Init_Session
from app.Schemes.Stock_Schemes import Stock_Scheme_Part, Stock_Scheme_Raw_Coponent, Stock_Scheme_machined_Coponent, Stock_Transfer_Scheme
from app.repositories.Relation_repositorie import Relation_repositorie
from app.repositories.Stock_repositorie import Stock_repositorie
from app.repositories.Components_repositorie import Components_Repositorie
from app.repositories.Parts_repositorie import Parts_Repositorie
from app.repositories.Sectors_repositorie import Sectors_repositorie
from app.Services.Stock_Services import Stock_Services
from app.domain.Exceptions import NotFoundException
from app.core.Dependecies import Verify_Token
from app.repositories.Movimentation_repositorie import MovimentationRepository
from app.repositories.PartAndComp_repositorie import PartsAndComp_Repositorie

Stock_Router = APIRouter(prefix="/stock", tags=["Stock Operation"])


@Stock_Router.post("/Create_Stock")
async def create_stock_part(scheme:Stock_Scheme_Part,session:Session = Depends(Init_Session), employer_id: int = Depends(Verify_Token)):
    stock_repo = Stock_repositorie(session=session)
    sectors_repo = Sectors_repositorie(session=session)
    partsandcomp_repo = PartsAndComp_Repositorie(session=session)
    relation_repo = Relation_repositorie(session=session)
    movimentation_repo = MovimentationRepository(session=session)
    service = Stock_Services(repo=stock_repo, sectors_repo=sectors_repo, partsAndComp_repo=partsandcomp_repo, relation_repo=relation_repo, movimentation_repo=movimentation_repo)
    try:
        new_stock = service.Service_Create_Stock(scheme=scheme, employer_id=employer_id)
        return {"message": "Stock created successfully",
                "Stock": new_stock }
    except NotFoundException as e:
        raise HTTPException(detail=str(e), status_code=404)

@Stock_Router.get("/Get_all_stock")
async def get_all_stock(session:Session = Depends(Init_Session)):
    stock_repo = Stock_repositorie(session=session)
    service = Stock_Services(repo=stock_repo)
    try:
        stock = service.service_get_all_stock()
        return stock
    except NotFoundException as e:
        raise HTTPException(detail=str(e), status_code=404)

@Stock_Router.get("/Get_filtered_stock")
async def get_filtered_stock(part_number:str = None,
                             status:str = None,
                             sector_id: int = None,
                             batch: str = None,
                             machining_batch: str = None,
                             assembly_batch: str = None,
                             session:Session = Depends(Init_Session)):
    stock_repo = Stock_repositorie(session=session)
    service = Stock_Services(repo=stock_repo)
    try:
        stock = service.service_get_filtered_stock(part_number=part_number, status=status, sector_id=sector_id)
        return stock
    except NotFoundException as e:
        raise HTTPException(detail=str(e), status_code=404)
    

@Stock_Router.delete("/Delete_stock/{stock_id}")
async def delete_stock(stock_id:int, session:Session = Depends(Init_Session)):
    stock_repo = Stock_repositorie(session=session)
    service = Stock_Services(repo=stock_repo)
    try:
        delete = service.Service_delete_stock(stock_id=stock_id)
        return {"message": "Stock deleted successfully",
                "Deleted": delete }
    except NotFoundException as e:
        raise HTTPException(detail=str(e), status_code=404)
    

@Stock_Router.patch("/Transfer_stock/{stock_id}")
async def transfer_stock(scheme:Stock_Transfer_Scheme, session:Session = Depends(Init_Session), employer_id: int = Depends(Verify_Token)):
    stock_repo = Stock_repositorie(session=session)
    sectors_repo = Sectors_repositorie(session=session)
    parts_repo = Parts_Repositorie(session=session)
    components_repo = Components_Repositorie(session=session)
    movimentation_repo = MovimentationRepository(session=session)
    service = Stock_Services(repo=stock_repo, sectors_repo=sectors_repo, movimentation_repo=movimentation_repo, parts_repo=parts_repo, components_repo=components_repo)
    try:
        transfered_stock = service.Service_Transfer_Stock(scheme=scheme, employer_id=employer_id)
        return {"message": "Stock transferred successfully",
                "Stock": transfered_stock }
    except NotFoundException as e:
        stock_repo.transaction_rollback()
        raise HTTPException(detail=str(e), status_code=404)