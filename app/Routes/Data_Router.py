from fastapi import APIRouter, Depends, HTTPException
from app.core.Dependecies import Init_Session
from sqlalchemy.orm import Session
from app.Schemes.Parts_Schemes import Components_Scheme, Parts_Scheme, Components_Scheme_Update, Clients_Scheme, Clients_Update_Scheme, parts_Update_Scheme
from app.models.Models import Components, Parts, componentsAndparts
from app.Services.Data_Services import  add_components, add_parts, get_components, update_components, update_parts, get_parts
from app.Services.Client_Services import add_clients, update_clients, get_clients
Data_Router = APIRouter(prefix="/data", tags=["Data Operations"])

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