#FastAPI
from fastapi import APIRouter, Depends, HTTPException
#SQLAlchemy
from sqlalchemy.orm import Session
#Schema and Response
from app.Schemas.Sector_Schemas import SectorSchema, UpdateSectorInfoSchema
from app.Schemas.Responses.Response_Sector import ResponseSector
#Service
from app.Services.Sector_Service import Sectors_Services
#Repository
from app.repositories.Sectors_repository import SectorsRepository
#Dependecies
from app.core.Dependecies import Init_Session
#Exceptions
from app.domain.Exceptions import AlreadyExist, NotFoundException


Sector_Router = APIRouter(prefix="/sector", tags=["Sectors Operation"])

@Sector_Router.post("/post_sector")
async def post_sectors(scheme: SectorSchema, 
                       session: Session = Depends(Init_Session)
                       ):
    
    repo = SectorsRepository(session=session)
    service = Sectors_Services(repo=repo)

    try:
        new_sector = service.post_sector(scheme=scheme)

        return {"message":"Sector created successfuly"}
    
    except AlreadyExist as e:
        raise HTTPException(status_code=409, detail=str(e))
    
    

@Sector_Router.get("/get_sectors")
async def get_all_sectors(session: Session = Depends(Init_Session)):

    repo = SectorsRepository(session=session)
    service = Sectors_Services(repo=repo)

    try:
        sectors =  service.get_sectors()

        return sectors
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Sector_Router.get("/get_sector/{sector}", 
                   response_model=ResponseSector
                   )
async def get_sector_id(sector: str, 
                        session: Session = Depends(Init_Session)
                        ):
    
    repo = SectorsRepository(session=session)
    service = Sectors_Services(repo=repo)

    try:
        sector =  service.get_sector_by_name(sector=sector)

        return sector
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@Sector_Router.patch("/update_sector/{sector}")
async def update_sector(sector:str, scheme:UpdateSectorInfoSchema, 
                        session:Session = Depends(Init_Session)
                        ):
    
    repo = SectorsRepository(session=session)
    service = Sectors_Services(repo=repo)

    try:
        sector =  service.update_sector_info(sector=sector, scheme=scheme)

        return sector
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@Sector_Router.delete("/Delete_sector/{sector}")
async def delete_sector(sector:str, 
                        session:Session=Depends(Init_Session)):
    
    repo = SectorsRepository(session=session)
    service = Sectors_Services(repo=repo)

    try:
        sector =  service.delete_sector(sector=sector)
        return {"message":"Sector deleted successfuly"}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))