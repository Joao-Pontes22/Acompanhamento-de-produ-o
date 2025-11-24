from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Models.Models import Stocks
from Dependecies import Init_Session

Stock_Router = APIRouter(prefix="/stock", tags=["Stock"])

@Stock_Router.post("/add_stock")
async def add_stock(session: Session =Depends(Init_Session)):