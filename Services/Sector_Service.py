from fastapi import Depends
from sqlalchemy.orm import Session
from models.Models import Sectors
from Dependecies import Init_Session

#---------------------// SECTOR OPERATIONS //---------------------#
async def get_sectors(session: Session = Depends(Init_Session)):
    sectors = session.query(Sectors).all()
    return sectors
async def get_sector_by_id(sector_id: int, session: Session = Depends(Init_Session)):
    sector = session.query(Sectors).filter(Sectors.ID == sector_id).first()
    return sector

async def post_sector(name_sector: str, tag_sector: str, session: Session = Depends(Init_Session)):
    new_sector = Sectors(sector=name_sector.upper(), tag=tag_sector.upper())
    session.add(new_sector)
    session.commit()
    return new_sector