from fastapi import APIRouter, Depends, HTTPException
from Dependecies import Init_Session
from sqlalchemy.orm import Session
from Schemes.Data_Schemes import Components_Scheme, Parts_Scheme, Components_Scheme_Update, Clients_Scheme, Clients_Update_Scheme, parts_Update_Scheme
from Models.Models import Components, Parts
from Services.Data_Services import add_clients, add_components, add_parts, get_clients, get_components, update_clients, update_components, update_parts, get_parts


Data_Router = APIRouter(prefix="/data", tags=["Data Operations"])

@Data_Router.post("/add_component")
async def add_component(scheme: Components_Scheme,session: Session = Depends(Init_Session)):
    return await add_components(scheme=scheme, session=session)

@Data_Router.get("/get_components")
async def get_component(description: str = None , 
                         part_number: str = None, 
                         supplier_ID: int = None, 
                         session: Session = Depends(Init_Session)):
    return await get_components(description=description, 
                                part_number=part_number, 
                                supplier_ID=supplier_ID, 
                                session=session)

@Data_Router.put("/update_component/{id}")
async def update_component(id: int, scheme: Components_Scheme_Update, session: Session = Depends(Init_Session)):
    return await update_components(id=id, scheme=scheme, session=session)


@Data_Router.post("/add_parts")
async def add_part(schemes: Parts_Scheme, session: Session = Depends(Init_Session)):
    return await add_parts(schemes=schemes, session=session)
    
@Data_Router.get("/get_parts")
async def get_part(session: Session = Depends(Init_Session)):
    return await get_parts(session=session)

@Data_Router.put("/update_part/{id}")
async def update_part(id: int, scheme: parts_Update_Scheme, session: Session = Depends(Init_Session)):
     return await update_parts(id=id, scheme=scheme, session=session)

@Data_Router.post("/add_client")
async def add_client(scheme: Clients_Scheme, session: Session = Depends(Init_Session)):
    return await add_clients(scheme=scheme, session=session)

@Data_Router.get("/get_clients")
async def get_client(session: Session = Depends(Init_Session)):
    return await get_clients(session=session)

@Data_Router.put("/update_client/{id}")
async def update_client(id: int, scheme: Clients_Update_Scheme, session: Session = Depends(Init_Session)):
    return await update_clients(id=id, scheme=scheme, session=session)