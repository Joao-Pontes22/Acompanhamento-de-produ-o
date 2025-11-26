from fastapi import APIRouter, Depends, HTTPException
from Dependecies import Init_Session
from sqlalchemy.orm import Session
from Schemes.Data_Schemes import Components_Scheme, Parts_Scheme
from Models.Models import Components, Parts

Data_Router = APIRouter(prefix="/data", tags=["Data Operations"])

@Data_Router.post("/add_component")
async def add_component(scheme: Components_Scheme,session: Session = Depends(Init_Session)):
    new_component = Components(
        part_number=scheme.part_number,
        description_material=scheme.description_material,
        supplier_ID=scheme.supplier_ID,
        cost=scheme.cost
    )
    session.add(new_component)
    session.commit()
    session.refresh(new_component)
    return {"message": "Component added successfully", "component": new_component}

@Data_Router.post("/add_parts")
async def add_parts(schemes: Parts_Scheme, session: Session = Depends(Init_Session)):
    new_parts = Parts(part_number=schemes.part_number,
                      description_parts=schemes.description_parts,
                      clients_ID=schemes.clients_ID,
                      cost=schemes.cost
                      )
    session.add(new_parts)
    session.commit()
    return {"message": "Parts added successfully", "parts": new_parts}

@Data_Router.get("/get_components")
async def get_components(description: str = None , 
                         part_number: str = None, 
                         supplier_ID: int = None, 
                         session: Session = Depends(Init_Session)):
    components = session.query(Components).all()
    if description is not None:
        components = session.query(Components).filter(Components.description_material.ilike(f"%{description}%")).all()
    if part_number is not None:
        components = session.query(Components).filter(Components.part_number == part_number).all()
    if supplier_ID is not None:
        components = session.query(Components).filter(Components.supplier_ID == supplier_ID).all()

    if  part_number and  supplier_ID and description is None:
        components = session.query(Components).all()
    if not components:
        raise HTTPException(status_code=404, detail="No components found with the given criteria")
    return components