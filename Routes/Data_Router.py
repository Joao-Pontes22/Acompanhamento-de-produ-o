from fastapi import APIRouter, Depends
from Dependecies import Init_Session
from sqlalchemy.orm import Session


Data_Router = APIRouter(prefix="/data", tags=["Data Operations"])

@Data_Router.post("/add_component")
async def add_component(session: Session = Depends(Init_Session)):