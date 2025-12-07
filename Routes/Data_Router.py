from fastapi import APIRouter, Depends, HTTPException
from Dependecies import Init_Session
from sqlalchemy.orm import Session
from Schemes.Data_Schemes import Components_Scheme, Parts_Scheme, Components_Scheme_Update, Clients_Scheme, Clients_Update_Scheme, parts_Update_Scheme
from models.Models import Components, Parts, componentsAndparts
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

@Data_Router.get("/getcomponentsandparts")
async def get_componentsandparts(session: Session = Depends(Init_Session)):
    componentsandparts = session.query(componentsAndparts).all()
    if not componentsandparts:
        raise HTTPException(status_code=404, detail="No components and parts found")
    return componentsandparts

@Data_Router.put("/updatecomponentsandparts/{id}")
async def update_componentsandparts(session: Session = Depends(Init_Session)):
    components = session.query(Components).all()
    parts = session.query(Parts).all()
    for comp in components:
        comps = session.query(componentsAndparts).filter(componentsAndparts.part_number == comp.part_number).first()
        comps.cost = comp.cost
    for part in parts:
        parts_ = session.query(componentsAndparts).filter(componentsAndparts.part_number == part.part_number).first()
        parts_.cost = part.cost
    session.commit()
    return {"message": "Component or Part updated successfully"}