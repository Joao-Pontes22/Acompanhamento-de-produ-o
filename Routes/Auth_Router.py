from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Schemes.Responses.Response_Auth import Response_Auth
from Schemes.Auth_Schemes import Auth_Scheme, Auth_Scheme_Update
from Services.Auth_Services import post_employer, get_all_employers, get_employer_id
from Dependecies import Init_Session
from Services.Sector_Service import get_sectors
Auth_Router = APIRouter(prefix="/auth", tags=["Auth"])

@Auth_Router.post("/Create_User")
async def create_user(Auth_Data: Auth_Scheme, session: Session = Depends(Init_Session)):
    new_employer = await post_employer(Auth_Data=Auth_Data, session=session)
    return {"message": "User created successfully", "name": new_employer.name}

@Auth_Router.get("/Get_Employers", response_model=list[Response_Auth])
async def get_auth(session: Session = Depends(Init_Session)):
    employers = await get_all_employers(session=session)
    return [
        {
            "name": employer.name,
            "ID": employer.ID,
            "sector_name": employer.employer_sector.sector,
            "sector_tag": employer.employer_sector.tag
            
        }
        for employer in employers
    ]

@Auth_Router.get("/Get_Employers/{id}", response_model=Response_Auth)
async def get_auth_name(id: int, session: Session = Depends(Init_Session)):
    employer = await get_employer_id(employer_id=id, session=session)
    return {
                "name": employer.name,
                "ID": employer.ID,
                "sector_name": employer.employer_sector.sector,
                "sector_tag": employer.employer_sector.tag
            }
        
@Auth_Router.put("/Update_Employer/{id}")
async def update_employer(id:int,scheme: Auth_Scheme_Update, session: Session = Depends(Init_Session)):
    employer = await get_employer_id(employer_id=id,session=session)
    if scheme.name is not None:
        employer.name = scheme.name.upper()
    if scheme.sector_ID is not None:
        employer.sector_ID = scheme.sector_ID
    session.commit()
    return {"message": "Employer updated successfully", 
                    "name": employer.name,
                    "sector_ID": employer.sector_ID,
                    "sector_name": employer.employer_sector.sector,
                    "sector_tag": employer.employer_sector.tag
                    }

@Auth_Router.delete("/Delete_Employer/{name}")
async def delete_employer(id: int, session: Session = Depends(Init_Session)):
    employers = await get_employer_id(employer_id=id, session=session)
    for employer in employers:
        if employer.ID == id:
            session.delete(employer)
            session.commit()
            return {"message": "Employer deleted successfully", "name": employer.name}