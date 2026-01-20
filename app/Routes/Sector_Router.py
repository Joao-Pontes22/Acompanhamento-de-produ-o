from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.Schemes.Sector_Schemes import Sector_Scheme, Sector_Scheme_Update
from app.Schemes.Responses.Responde_Sector import Response_Sector
from app.Services.Sector_Service import Sectors_Services
from app.repositories.Sectors_repository import Sectors_repositorie
from app.core.Dependecies import Init_Session
from app.domain.Exceptions import AlreadyExist, NotFoundException


Sector_Router = APIRouter(prefix="/sector", tags=["Sectors Operation"])

@Sector_Router.post("/post_sector")
async def post_sectors(scheme: Sector_Scheme, session: Session = Depends(Init_Session)):
    repo = Sectors_repositorie(session=session)
    service = Sectors_Services(repo=repo)
    try:
        new_sector = service.service_post_sector(scheme=scheme)
        return {"message":"Sector created successfuly"}
    except AlreadyExist as e:
        raise HTTPException(status_code=409, detail=str(e))
    
    

@Sector_Router.get("/get_sectors")
async def get_all_sectors(session: Session = Depends(Init_Session)):
    repo = Sectors_repositorie(session=session)
    service = Sectors_Services(repo=repo)
    try:
        sectors =  service.service_get_sectors()
        return sectors
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Sector_Router.get("/get_sector/{sector}", response_model=Response_Sector)
async def get_sector_id(sector: str, session: Session = Depends(Init_Session)):
    repo = Sectors_repositorie(session=session)
    service = Sectors_Services(repo=repo)
    try:
        sector =  service.service_get_sector_by_name(sector=sector)
        return sector
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@Sector_Router.patch("/update_sector/{sector}")
async def update_sector(sector:str, scheme:Sector_Scheme_Update, session:Session = Depends(Init_Session)):
    repo = Sectors_repositorie(session=session)
    service = Sectors_Services(repo=repo)
    try:
        sector =  service.service_update_sector_info(sector=sector, scheme=scheme)
        return sector
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@Sector_Router.delete("/Delete_sector/{sector}")
async def delete_sector(sector:str, session:Session=Depends(Init_Session)):
    repo = Sectors_repositorie(session=session)
    service = Sectors_Services(repo=repo)
    try:
        sector =  service.service_delete_sector(sector=sector)
        return {"message":"Sector deleted successfuly"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))