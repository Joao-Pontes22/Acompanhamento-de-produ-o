from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.core.Dependecies import Init_Session
from app.Schemes.Parts_Schemes import Components_Scheme, Parts_Scheme, Components_Scheme_Update, Clients_Scheme, Clients_Update_Scheme, parts_Update_Scheme
from app.models.Models import Clients, Components, Parts, componentsAndparts

x
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

async def get_parts(session: Session = Depends(Init_Session)):
    parts = session.query(Parts).all()
    return parts


async def add_parts(schemes: Parts_Scheme, session: Session = Depends(Init_Session)):
    new_parts = Parts(part_number=schemes.part_number.upper(),
                      description_parts=schemes.description_parts.upper(),
                      clients_ID=schemes.clients_ID,
                      cost=schemes.cost
                      )
    new_parts2 = componentsAndparts(part_number=schemes.part_number.upper(),
                                    description=schemes.description_parts.upper(),
                                    category="PART",
                                    cost=schemes.cost
                                    )
    session.add(new_parts)
    session.add(new_parts2)
    session.commit()
    return {"message": "Parts added successfully", "parts": new_parts}