from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.Models import Stock
from app.core.Dependecies import Init_Session
from app.Services.Stock_Services import add_stock, get_all_stock
from app.Schemes.Stock_Schemes import Stock_Scheme_warehouse

Stock_Router = APIRouter(prefix="/stock", tags=["Stock Operation"])

@Stock_Router.post("/add_stock")
async def add_stocks(scheme: Stock_Scheme_warehouse, session: Session =Depends(Init_Session)):
    return await add_stock(scheme=scheme, session=session)

@Stock_Router.get("/get_all_stock")
async def get_stocks(session: Session = Depends(Init_Session)):
    return await get_all_stock(session=session)