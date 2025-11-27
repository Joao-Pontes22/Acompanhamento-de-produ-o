from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Schemes.Sector_Schemes import Sector_Scheme, Sector_Scheme_Update
from Schemes.Responses.Responde_Sector import Response_Sector
from Services.Sector_Service import get_sectors, post_sector, get_sector_by_id
from Dependecies import Init_Session
Sector_Router = APIRouter(prefix="/sector", tags=["Sector"])

@Sector_Router.post("/post_sector")
async def post_sectors(scheme: Sector_Scheme, session: Session = Depends(Init_Session)):
    new_sector = await post_sector(name_sector=scheme.sector, tag_sector=scheme.tag, session=session)
    return {"message": "Sector added successfully",
            "Sector": new_sector}

@Sector_Router.get("/get_sectors")
async def get_all_sectors(session: Session = Depends(Init_Session)):
    sectors = await get_sectors(session=session)
    return sectors

@Sector_Router.get("/get_sector/{id}", response_model=Response_Sector)
async def get_sector_id(id: int, session: Session = Depends(Init_Session)):
    sector = await get_sector_by_id(sector_id=id,session=session)
    return sector

@Sector_Router.put("/get_sector/{id}", response_model=Response_Sector)
async def get_sector_id(id: int, scheme: Sector_Scheme_Update,session: Session = Depends(Init_Session)):
    sector = await get_sector_by_id(sector_id=id,session=session)
    if sector:
        if scheme.sector is not None:
            sector.sector = scheme.sector.upper()
        if scheme.tag is not None:
            sector.tag = scheme.tag.upper()
        session.commit()
    return sector

@Sector_Router.delete("/delete_sector/{id}")
async def delete_sector(id: int, session: Session = Depends(Init_Session)):
    sector = await get_sector_by_id(sector_id=id, session=session)
    if sector:
        session.delete(sector)
        session.commit()
        return {"message": "Sector deleted successfully", "sector": sector.sector}