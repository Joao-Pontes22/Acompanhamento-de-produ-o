from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.Models import Stock
from app.core.Dependecies import Init_Session
from app.Schemes.Stock_Schemes import Stock_Scheme_warehouse

Stock_Router = APIRouter(prefix="/stock", tags=["Stock Operation"])

