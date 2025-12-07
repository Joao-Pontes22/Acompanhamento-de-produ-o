from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from Dependecies import Init_Session
from Schemes.Data_Schemes import Components_Scheme, Parts_Scheme, Components_Scheme_Update, Clients_Scheme, Clients_Update_Scheme, parts_Update_Scheme
from models.Models import Clients, Components, Parts, componentsAndparts

async def add_components(scheme: Components_Scheme,session: Session = Depends(Init_Session)):
    new_component = Components(
        part_number=scheme.part_number.upper(),
        description_material=scheme.description_material.upper(),
        supplier_ID=scheme.supplier_ID,
        cost=scheme.cost
    )
    new_component2 = componentsAndparts(part_number=scheme.part_number.upper(),
                                        description_material=scheme.description_material.upper(),
                                        category="COMPONENT",
                                        cost=scheme.cost
                                        )
    session.add(new_component)
    session.add(new_component2)
    session.commit()
    session.refresh(new_component)
    return {"message": "Component added successfully", "component": new_component}

async def add_parts(schemes: Parts_Scheme, session: Session = Depends(Init_Session)):
    new_parts = Parts(part_number=schemes.part_number.upper(),
                      description_parts=schemes.description_parts.upper(),
                      clients_ID=schemes.clients_ID,
                      cost=schemes.cost
                      )
    new_parts2 = componentsAndparts(part_number=schemes.part_number.upper(),
                                    description_material=schemes.description_parts.upper(),
                                    category="PART",
                                    cost=schemes.cost
                                    )
    session.add(new_parts)
    session.add(new_parts2)
    session.commit()
    return {"message": "Parts added successfully", "parts": new_parts}

async def get_components(description: str = None , 
                         part_number: str = None, 
                         supplier_ID: int = None, 
                         session: Session = Depends(Init_Session)):
    components = session.query(Components).all()
    if description is not None:
        components = session.query(Components).filter(Components.description_material.ilike(f"%{description.upper()}%")).all()
    if part_number is not None:
        components = session.query(Components).filter(Components.part_number == part_number.upper()).all()
    if supplier_ID is not None:
        components = session.query(Components).filter(Components.supplier_ID == supplier_ID).all()

    if  part_number and  supplier_ID and description is None:
        components = session.query(Components).all()
    if not components:
        raise HTTPException(status_code=404, detail="No components found with the given criteria")
    return components

async def update_components(id: int, scheme: Components_Scheme_Update, session: Session = Depends(Init_Session)):
    component = session.query(Components).filter(Components.ID == id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    if scheme.part_number is not None:
        component.part_number = scheme.part_number.upper()
    if scheme.description_material is not None:
        component.description_material = scheme.description_material.upper()
    if scheme.supplier_ID is not None:
        component.supplier_ID = scheme.supplier_ID
    if scheme.cost is not None:
        component.cost = scheme.cost
    session.commit()
    return {"message": "Component updated successfully", "component": component}

async def update_parts(id: int, scheme: parts_Update_Scheme, session: Session = Depends(Init_Session)):
    part = session.query(Parts).filter(Parts.ID == id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    if scheme.part_number is not None:
        part.part_number = scheme.part_number.upper()
    if scheme.description_parts is not None:
        part.description_parts = scheme.description_parts.upper()
    if scheme.clients_ID is not None:
        part.clients_ID = scheme.clients_ID
    if scheme.cost is not None:
        part.cost = scheme.cost
    session.commit()
    return {"message": "Part updated successfully", "part": part}

async def add_clients(scheme: Clients_Scheme, session: Session = Depends(Init_Session)):
    new_client = Clients(
        name=scheme.name.upper(),
        contact=scheme.contact.upper(),
        email=scheme.email.lower(),
        phone=scheme.phone
    )
    session.add(new_client)
    session.commit()
    session.refresh(new_client)
    return {"message": "Client added successfully", "client": new_client}

async def get_clients(session: Session = Depends(Init_Session)):
    clients = session.query(Clients).all()
    return clients

async def get_parts(session: Session = Depends(Init_Session)):
    parts = session.query(Parts).all()
    return parts

async def update_clients(id: int, scheme: Clients_Update_Scheme, session: Session = Depends(Init_Session)):
    client = session.query(Clients).filter(Clients.ID == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    if scheme.name is not None:
        client.name = scheme.name.upper()
    if scheme.contact is not None:
        client.contact = scheme.contact.upper()
    if scheme.email is not None:
        client.email = scheme.email.lower()
    if scheme.phone is not None:
        client.phone = scheme.phone
    session.commit()
    return {"message": "Client updated successfully", "client": client}
