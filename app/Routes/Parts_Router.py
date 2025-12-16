from fastapi import APIRouter, Depends, HTTPException
from app.core.Dependecies import Init_Session
from sqlalchemy.orm import Session
from app.Schemes.Parts_Schemes import Components_Scheme, Parts_Scheme, Components_Scheme_Update, Clients_Scheme, Clients_Update_Scheme, parts_Update_Scheme
from app.models.Models import Components, Parts, componentsAndparts
from app.Services.Data_Services import  add_components, add_parts, get_components, update_components, update_parts, get_parts
from app.Services.Client_Services import add_clients, update_clients, get_clients

Data_Router = APIRouter(prefix="/Parts", tags=["Parts Operations"])
                

@Data_Router.post("/add_parts")
async def add_part(schemes: Parts_Scheme, session: Session = Depends(Init_Session)):
    return await add_parts(schemes=schemes, session=session)
    
@Data_Router.get("/get_parts")
async def get_part(session: Session = Depends(Init_Session)):
    return await get_parts(session=session)

@Data_Router.put("/update_part/{id}")
async def update_part(id: int, scheme: parts_Update_Scheme, session: Session = Depends(Init_Session)):
     return await update_parts(id=id, scheme=scheme, session=session)