from fastapi import APIRouter, Depends
from Models.Models import Sectors
from sqlalchemy.orm import Session
from Settings.Settings import get_sectors
from Dependecies import Init_Session
Sector_Router = APIRouter(prefix="/sector", tags=["Sector"])

@Sector_Router.post("/post_sector")
async def post_sector(name_sector: str, tag_sector: str, session: Session = Depends(Init_Session)):
    new_sector = Sectors(sector=name_sector.upper(), tag=tag_sector.upper())
    session.add(new_sector)
    session.commit()
    return {"message": "Sector added successfully",
            "Sector": {
                "name": new_sector.sector,
                "tag": new_sector.tag}}

@Sector_Router.get("/get_sectors")
async def get_all_sectors(session: Session = Depends(Init_Session)):
    sectors = await get_sectors(session=session)
    return sectors