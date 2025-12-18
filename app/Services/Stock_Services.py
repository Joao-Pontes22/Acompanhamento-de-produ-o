from fastapi import  Depends
from sqlalchemy.orm import Session
from app.models.Models import Stock, ComponentsAndParts
from app.core.Dependecies import Init_Session
from app.Schemes.Stock_Schemes import Stock_Scheme_warehouse

class Stock_Services:
    def __init__(self, repo):
        pass
