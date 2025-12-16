from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.Schemes.Sector_Schemes import Sector_Scheme, Sector_Scheme_Update
from app.Schemes.Responses.Responde_Sector import Response_Sector
from app.Services.Sector_Service import Sectors_Services
from app.repositories.Sectors_repositorie import Sectors_repositorie
from app.core.Dependecies import Init_Session
Sector_Router = APIRouter(prefix="/sector", tags=["Sectors Operation"])

@Sector_Router.post("/post_sector")
async def post_sectors(scheme: Sector_Scheme, session: Session = Depends(Init_Session)):
    repo = Sectors_repositorie(session=session)
    service = Sectors_Services(repo=repo)
    new_sector = service.service_post_sector(scheme=scheme)
    return new_sector

@Sector_Router.get("/get_sectors")
async def get_all_sectors(session: Session = Depends(Init_Session)):
    repo = Sectors_repositorie(session=session)
    service = Sectors_Services(repo=repo)
    sectors =  service.service_get_sectors()
    return sectors

@Sector_Router.get("/get_sector/{id}")
async def get_sector_id(id: int, session: Session = Depends(Init_Session)):
    repo = Sectors_repositorie(session=session)
    service = Sectors_Services(repo=repo)
    sector =  service.service_get_sector_by_id(sector_id=id)
    return sector

@Sector_Router.patch("/update_sector")
async def update_sector(id:int, scheme:Sector_Scheme_Update, session:Session = Depends(Init_Session)):
    repo = Sectors_repositorie(session=session)
    service = Sectors_Services(repo=repo)
    sector =  service.service_update_sector_info(id=id, scheme=scheme)
    return sector

@Sector_Router.delete("/Delete_sector")
async def delete_sector(id:int, session:Session=Depends(Init_Session)):
    repo = Sectors_repositorie(session=session)
    service = Sectors_Services(repo=repo)
    sector =  service.service_delete_sector(id=id)